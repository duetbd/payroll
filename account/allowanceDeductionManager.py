from django.shortcuts import render, redirect
from django.views.generic import  DetailView, View
from django.core.urlresolvers import reverse_lazy

from .forms import EmployeeAllowanceDeductionForm, AllowanceDeductionEmployeeClassValueForm, ConfigureAllowanceDeductionForm

from employee.models import Employee
from .models import AllowanceDeduction, EmployeeAllowanceDeduction, EmployeeClass, AllowanceDeductionEmployeeClassValue

from duet_admin.utils import PageFilteredTableView, AddTableMixin,CustomUpdateView


class AllowanceDeductionList(AddTableMixin, PageFilteredTableView):
	model = AllowanceDeduction
	template_name = 'account/list.html'

	exclude=['id', 'code', 'created_at', 'modified_at']
	filter_fields = {
		'name' : ['icontains'],
		'category': ['exact'],
	}
	title = 'Pay, Allowances and Deductions List'
	actions = [ 
		{'url' : 'account:allowance-deduction-detail', 'tooltip' : 'Detail', 'icon' : 'glyphicon glyphicon-th-large'},
		{'url' : 'account:configure-allowance-deduction-employee-class', 'tooltip' : 'Configure Default Values', 'icon' : 'glyphicon glyphicon-cog'},
		{'url' : 'account:allowance-deduction-update', 'tooltip' : 'Edit',  'icon' : 'glyphicon glyphicon-pencil'}
		]

	add_link = [
		{ 'url' : 'account:configure-allowance-deduction', 'icon' : 'glyphicon glyphicon-cog'}
		]

class AllowanceDeductionDetail(DetailView):
	model = AllowanceDeduction
	template_name = 'account/allowanceDeduction/detail.html'
	context_object_name = 'allowanceDeduction'


class ConfigureEmployeeAllowanceDeduction(View):
	template_name = 'allowanceDeduction/employeeAllowance.html'

	def createFormset(self,request, allowance_deductions , prefix, employee): 
		formset = []
		employee_allowances = EmployeeAllowanceDeduction.objects.filter(employee = employee)
		for a in allowance_deductions:
			try:
				employee_allowance_deduction = employee_allowances.get(allowance_deduction = a)
			except EmployeeAllowanceDeduction.DoesNotExist:
				employee_allowance_deduction = EmployeeAllowanceDeduction()
			form = EmployeeAllowanceDeductionForm(request.POST or None, prefix = prefix +  str(a.id), instance = employee_allowance_deduction, allowance_deduction = a)
			formset.append(form)
		return formset

	def get(self, request, pk):
		employee = Employee.objects.get(pk = pk)
		allowance_deductions = AllowanceDeduction.objects.filter(is_applicable = True)
		allowances = allowance_deductions.exclude(category = 'd')
		deductions = allowance_deductions.filter(category = 'd')
		allowanace_formset = self.createFormset(request, allowances, 'allowance-', employee)
		deduction_formset  = self.createFormset(request, deductions, 'deduction-', employee)
		return render(request, 'account/allowanceDeduction/employeeAllowance.html', {'employee' : employee, 'allowanace_formset' : allowanace_formset, 'deduction_formset' : deduction_formset})

	def post(self, request, pk):
		employee = Employee.objects.get(pk = pk)
		allowance_deductions = AllowanceDeduction.objects.filter(is_applicable = True)
		allowances = allowance_deductions.exclude(category = 'd')
		deductions = allowance_deductions.filter(category = 'd')
		allowanace_formset = self.createFormset(request, allowances, 'allowance-', employee)
		deduction_formset = self.createFormset(request, deductions, 'deduction-', employee)
		formset = allowanace_formset + deduction_formset
		for form in formset:
			if form.is_valid():
				instance = form.save(commit = False)
				instance.employee = employee
				instance.save()
		return redirect('account:employee-detail', pk = employee.id)


class AllowanceDeductionUpdate(CustomUpdateView):
	model = AllowanceDeduction
	fields = [ 'description', 'is_percentage', 'is_applicable', 'payment_type']
	template_name = 'account/create.html'
	success_url = reverse_lazy('account:allowance-deduction-list')
	cancel_url = 'account:allowance-deduction-list'
	title = 'Edit - '


class ConfigureAllowanceDeductionEmployeeClassValue(View):
	def createFormset(self, request, employee_classes, allowance_deduction): 
		formset = []
		allownace_deduction_employee_class_values = AllowanceDeductionEmployeeClassValue.objects.filter(allowance_deduction = allowance_deduction)
		for _class in employee_classes:
			try:
				allowance_deduction_class_value = allownace_deduction_employee_class_values.get(employee_class = _class)
			except AllowanceDeductionEmployeeClassValue.DoesNotExist:
				allowance_deduction_class_value = AllowanceDeductionEmployeeClassValue()
			initial = {'amount' : allowance_deduction_class_value.amount}
			form = AllowanceDeductionEmployeeClassValueForm(request.POST or None, prefix = 'employee-class-' +  str(_class.id), instance = allowance_deduction_class_value, employee_class = _class, allowance_deduction = allowance_deduction, initial = initial)
			formset.append(form)
		return formset


	def get(self, request, pk):
		allowance_deduction = AllowanceDeduction.objects.get(pk = pk)
		employee_classes = EmployeeClass.objects.all()
		formset = self.createFormset(request, employee_classes, allowance_deduction)
		return render(request, 'account/allowanceDeduction/configureAllowanceDeductionEmployeeClass.html', {'allowanceDeduction' : allowance_deduction, 'formset' : formset})

	def post(self, request, pk):
		allowance_deduction = AllowanceDeduction.objects.get(pk = pk)
		employee_classes = EmployeeClass.objects.all()
		formset = self.createFormset(request, employee_classes, allowance_deduction)
		for form in formset:
			if form.is_valid():
				form.save()
		return redirect('account:allowance-deduction-list')



class ConfigureAllowanceDeduction(View):
	def createFormset(self,request, allowance_deductions , prefix): 
		formset = []
		for a in allowance_deductions:
			form = ConfigureAllowanceDeductionForm(request.POST or None, prefix = prefix +  str(a.id), instance = a)
			formset.append(form)
		return formset

	def get(self, request):
		allowance_deductions = AllowanceDeduction.objects.all()
		allowance_form_set = self.createFormset(request, allowance_deductions.exclude(category = 'd'), 'allowances')
		deduction_form_set = self.createFormset(request, allowance_deductions.filter(category = 'd'), 'deduction')
		return render(request, 'account/allowanceDeduction/configureAllowanceDeduction.html', {'allowanceFormSet' : allowance_form_set, 'deductionFormSet' : deduction_form_set})

	def post(self, request):
		allowance_deductions = AllowanceDeduction.objects.all()
		allowance_form_set = self.createFormset(request, allowance_deductions.exclude(category = 'd'), 'allowances')
		deduction_form_set = self.createFormset(request, allowance_deductions.filter(category = 'd'), 'deduction')
		formset = allowance_form_set + deduction_form_set
		for form in formset:
			if form.is_valid():
				form.save()
		return redirect('account:allowance-deduction-list')