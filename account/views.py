from django.shortcuts import render, redirect
from django.views.generic import  DetailView, DeleteView, View
from django.views.generic.detail import SingleObjectMixin, SingleObjectTemplateResponseMixin, BaseDetailView

from django.core.urlresolvers import reverse_lazy
from django.db.models import Sum

from .forms import  SalarySheetForm, SalarySheetDetailsForm, SalarySheetForm, SalarySheetDetailsEditForm

from employee.models import Employee
from .models import AllowanceDeduction, EmployeeAllowanceDeduction, SalarySheetDetails, SalarySheet, EmployeeClass, AllowanceDeductionEmployeeClassValue

from duet_admin.utils import PageFilteredTableView, AddTableMixin,CustomUpdateView, CustomCreateView

class EmployeeList(AddTableMixin, PageFilteredTableView):
	model = Employee
	template_name = 'account/employee/New/list.html'

	exclude=['created_at', 'modified_at', 'address', 'id', 'dob', 'gender', 'password', 'last_login', 'image']

	filter_fields = {
		'category' : ['exact'],
		'designation' : ['exact'],
		'name' : ['icontains'],
	}
	actions = [
		{'url' : 'account:employee-salary-sheet', 'icon' : 'glyphicon glyphicon-usd', 'tooltip' : 'Generate Salary Sheet'},
		{'url' : 'account:configure-employee-allowance-deduction', 'icon' : 'glyphicon glyphicon-cog', 'tooltip' : 'Configure Default Values'},
		{'url' : 'account:employee-detail', 'icon' : 'glyphicon glyphicon-th-large', 'tooltip' : 'Detail'},
	]

	title = 'Employee List'


class SalarySheetList(AddTableMixin, PageFilteredTableView):
	model = SalarySheet
	template_name = 'account/list.html'

	exclude=['id', 'comment']
	filter_fields = {
		'date' :  ['exact'],
		'employee__name': ['icontains'],
	}

	title = 'Salary Sheet List'

	actions = [
		{'url' : 'account:salary-sheet-detail', 'icon' : 'glyphicon glyphicon-th-large', 'tooltip' : 'Detail'},
		{'url' : 'account:salary-sheet-update', 'icon' : 'glyphicon glyphicon-pencil', 'tooltip' : 'Update'},
		{'url' : 'account:salary-sheet-confirm', 'icon' : 'glyphicon glyphicon-lock', 'tooltip' : 'Freeze'},
		{'url' : 'account:salary-sheet-delete', 'icon' : 'glyphicon glyphicon-trash', 'tooltip' : 'Delete'},
	]


class AccountEmployeeDetail(SalarySheetList):
	template_name = 'account/employee/detail.html'

	exclude=['id', 'comment', 'employee']
	filter_fields = {
		'date' :  ['exact'],
	}

	def get(self, request, *args, **kwargs):
		self.employee = Employee.objects.get(pk = kwargs.pop('pk'))
		return super().get(request, args, kwargs)


	def get_queryset(self, **kwargs):
		qs = super().get_queryset(**kwargs)
		employee = self.employee
		return qs.filter(employee = employee)


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		employee = self.employee
		context['employee'] = employee
		return context


class SalarySheetCreate(View):

	def createFormset(self,request, allowance_deductions , prefix, employee): 
		formset = []
		employee_class = employee.employee_class
		allowance_deduction_employee_class_values = AllowanceDeductionEmployeeClassValue.objects.filter(employee_class= employee_class)
		for a in allowance_deductions:
			initial = {'amount' : 0}
			try:
				allowance_deduction_class_value = allowance_deduction_employee_class_values.objects.get(allowance_deduction = a.allowance_deduction)
				initial['amount'] = allowance_deduction_class_value.amount
			except AttributeError:
				initial['amount'] = 0
			if a.value : 
				initial['amount'] = a.value
			form = SalarySheetDetailsForm(request.POST or None, prefix = prefix +  str(a.id), instance = SalarySheetDetails(), allowance_deduction = a.allowance_deduction, initial = initial)
			formset.append(form)
		return formset


	def get(self, request, pk):
		employee = Employee.objects.get(pk = pk)
		employee_allowance_deductions = EmployeeAllowanceDeduction.objects.filter(employee = employee,is_applicable= True, allowance_deduction__is_applicable=True)
		allowances = employee_allowance_deductions.exclude( allowance_deduction__category = 'd')
		deductions = employee_allowance_deductions.filter(allowance_deduction__category = 'd')

		salarySheetForm = SalarySheetForm(instance = SalarySheet())

		allowanace_formset = self.createFormset(request, allowances, 'allowance-', employee)
		deduction_formset = self.createFormset(request, deductions, 'deduction-', employee)

		return render(request, 'account/salarySheet/generateSheet.html', {'salary_sheet_form' : salarySheetForm,'employee' : employee, 'allowanace_formset' : allowanace_formset, 'deduction_formset' : deduction_formset})

	def post(self, request, pk):
		employee = Employee.objects.get(pk = pk)
		employee_allowance_deductions = EmployeeAllowanceDeduction.objects.filter(employee = employee, is_applicable= True, allowance_deduction__is_applicable=True)
		allowances = employee_allowance_deductions.exclude( allowance_deduction__category = 'd')
		deductions = employee_allowance_deductions.filter(allowance_deduction__category = 'd')

		salaryForm = SalarySheetForm(request.POST, instance = SalarySheet())
		
		allowanace_formset = self.createFormset(request, allowances, 'allowance-', employee)
		deduction_formset = self.createFormset(request, deductions, 'deduction-', employee)
		formset = allowanace_formset + deduction_formset

		salarySheet = salaryForm.save(commit = False)
		salarySheet.employee = employee
		salarySheet.save()
		for form in formset:
			if form.is_valid():
				instance = form.save(commit = False)
				instance.salary_sheet = salarySheet
				instance.employee = employee
				instance.save()
		return redirect('account:employee-detail', pk = employee.id)


class SalarySheetUpdate(View):
	
	def createFormset(self,request, allowance_deductions , prefix, employee): 
		formset = []
		for a in allowance_deductions:
			initial = {'amount' : a.amount}
			form = SalarySheetDetailsForm(request.POST or None, prefix = prefix +  str(a.id), instance = a, allowance_deduction = a.allowance_deduction, initial = initial)
			formset.append(form)
		return formset


	def get(self, request, pk):
		salary_sheet = SalarySheet.objects.get(pk = pk)
		if salary_sheet.is_freezed:
			return render(request, 'account/salarySheet/delete_not_allowed.html')
		employee = salary_sheet.employee
		salary_sheet_details = SalarySheetDetails.objects.filter(salary_sheet = salary_sheet)
		allowances = salary_sheet_details.exclude( allowance_deduction__category = 'd')
		deductions = salary_sheet_details.filter( allowance_deduction__category = 'd')
		
		allowanace_formset = self.createFormset(request, allowances, 'allowance-', employee)
		deduction_formset = self.createFormset(request, deductions, 'deduction-', employee)
		salary_sheet_form = SalarySheetForm(instance = salary_sheet)
		return render(request, 'account/salarySheet/generateSheet.html', {'salary_sheet_form' : salary_sheet_form, 'employee' : employee, 'allowanace_formset' : allowanace_formset, 'deduction_formset' : deduction_formset})

	def post(self, request, pk):
		salary_sheet = SalarySheet.objects.get(pk = pk)
		employee = salary_sheet.employee
		salary_sheet_details = SalarySheetDetails.objects.filter(salary_sheet = salary_sheet)
		allowances = salary_sheet_details.exclude( allowance_deduction__category = 'd')
		deductions = salary_sheet_details.filter( allowance_deduction__category = 'd')

		allowanace_formset = self.createFormset(request, allowances, 'allowance-', employee)
		deduction_formset = self.createFormset(request, deductions, 'deduction-', employee)
		formset = allowanace_formset + deduction_formset
		salaryForm = SalarySheetForm(request.POST, instance = salary_sheet)
		salaryForm.save()
		for form in formset:
			if form.is_valid():
				form.save()
		return redirect('account:employee-detail', pk = employee.id)

class SalarySheetDetail(DetailView):
	model = SalarySheet
	template_name = 'account/salarySheet/detail.html'
	context_object_name = 'salarSheet'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		salary_sheet = self.object
		total_payment = SalarySheetDetails.objects.filter(salary_sheet = salary_sheet).exclude(allowance_deduction__category = 'd').aggregate(total = Sum("amount"))['total']
		total_deduction = SalarySheetDetails.objects.filter(salary_sheet = salary_sheet).filter(allowance_deduction__category = 'd').aggregate(total = Sum("amount"))['total']
		if total_deduction is None:
			total_deduction = 0
		if total_payment is None:
			total_payment = 0
		context['allowances'] = SalarySheetDetails.objects.filter(salary_sheet = salary_sheet).exclude(allowance_deduction__category = 'd')
		context['deductions'] = SalarySheetDetails.objects.filter(salary_sheet = salary_sheet, allowance_deduction__category = 'd')
		context['totalPayment'] = total_payment
		context['totalDeduction'] = total_deduction 
		context['netPayment'] = total_payment - total_deduction
		context['employee'] = salary_sheet.employee
		return context

class SalarySheetDelete(DeleteView):
	model = SalarySheet
	success_url = reverse_lazy('account:salary-sheet-list')
	template_name = 'account/confirm_delete.html'

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.is_freezed:
			return render(request, 'account/salarySheet/delete_not_allowed.html')
		return super().get(request, args, kwargs)



class SalarySheetConfirm(SingleObjectTemplateResponseMixin, BaseDetailView):
	model = SalarySheet
	success_url = reverse_lazy('account:salary-sheet-list')
	template_name = 'account/confirm_delete.html'

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.is_freezed:
			return render(request, 'account/salarySheet/already_confirmed.html')
		return super().get(request, args, kwargs)

	def post(self, *args, **kwargs):
		salary_sheet = self.get_object()
		salary_sheet.is_freezed = True
		salary_sheet.save()
		return redirect('account:salary-sheet-list')





	
		
