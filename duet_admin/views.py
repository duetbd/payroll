from django.shortcuts import render
from django.views.generic import DetailView, DeleteView, View
from django.core.urlresolvers import reverse_lazy
from django.db.models import ProtectedError

from .forms import EmployeeCreateForm, EmployeeUpdateForm

from employee.models import Employee, Department, Designation, Employee
from account.models import AllowanceDeduction, Grade, EmployeeClass

from .utils import PageFilteredTableView, AddTableMixin, CustomUpdateView, CustomCreateView


####################################### Allowance Deduction ###############################################

class AllowanceDeductionList(AddTableMixin, PageFilteredTableView):
	model = AllowanceDeduction
	template_name = 'duet_admin/list.html'
	exclude=[ 'description', 'created_at', 'modified_at', 'id']
	filter_fields = {
		'name' : ['icontains'],
		'category' : ['exact'],
	}

	actions = [
		{'url' : 'duet_admin:allowancededuction-detail', 'icon' : 'glyphicon glyphicon-th-large', 'tooltip' : 'Detail'},
		{'url' : 'duet_admin:allowancededuction-update', 'icon' : 'glyphicon glyphicon-pencil', 'tooltip' : 'Update'},
		{'url' : 'duet_admin:allowancededuction-delete', 'icon' : 'glyphicon glyphicon-trash', 'tooltip' : 'Delete'},
	]

	title = 'Pay, Allowance and Deduction List'

	add_link = [
		{ 'url' : 'duet_admin:allowancededuction-create', 'icon' : 'glyphicon glyphicon-plus'}
		]

class AllowanceDeductionCreate(CustomCreateView):
	model = AllowanceDeduction
	fields = ['name', 'code','description', 'category', 'is_percentage', 'is_applicable', 'payment_type']
	template_name = 'duet_admin/create.html'
	cancel_url = 'duet_admin:allowancededuction-list'
	title = 'Create New Pay, Allowance or Deduction '

class AllowanceDeductionUpdate(CustomUpdateView):
	model = AllowanceDeduction
	fields = ['name','code', 'description', 'category', 'is_percentage', 'is_applicable', 'payment_type']
	template_name = 'duet_admin/create.html'
	cancel_url = 'duet_admin:allowancededuction-list'
	title = 'Edit - '

class AllowanceDeductionDetail(DetailView):
	model = AllowanceDeduction
	template_name = 'duet_admin/allowanceDeduction/detail.html'
	context_object_name = 'allowanceDeduction'
	
class AllowanceDeductionDelete(DeleteView):
	model = AllowanceDeduction
	success_url = reverse_lazy('duet_admin:allowancededuction-list')
	template_name = 'duet_admin/confirm_delete.html'

	def delete(self, request, *args, **kwargs):
		try:
			super().delete(request, *args, **kwargs)
		except ProtectedError:
			return render(request, 'common/protection_error.html')
		


####################################### Employee ##############################################################


class EmployeeCreate(CustomCreateView):
	template_name = 'duet_admin/create.html'
	form_class = EmployeeCreateForm
	model = Employee
	title = 'Create New Employee'
	cancel_url = 'duet_admin:employee-list'


class EmployeeList(AddTableMixin, PageFilteredTableView):
	model = Employee
	template_name = 'duet_admin/list.html'

	exclude=['address', 'tax_id_number','image', 'account_number', 'joining_date', 'password', 'last_login', 'category']
	filter_fields = {
		'designation' : ['exact'],
		'name' : ['icontains'],
	}

	actions = [
		{'url' : 'duet_admin:employee-detail', 'icon' : 'glyphicon glyphicon-th-large', 'tooltip' : 'Detail'},
		{'url' : 'duet_admin:employee-update', 'icon' : 'glyphicon glyphicon-pencil', 'tooltip' : 'Update'},
		{'url' : 'duet_admin:employee-delete', 'icon' : 'glyphicon glyphicon-trash', 'tooltip' : 'Delete'},
	]

	title = 'Employee List'

	add_link = [
		{ 'url' : 'duet_admin:employee-create', 'icon' : 'glyphicon glyphicon-plus'}
		]


class EmployeeUpdate(CustomUpdateView):
	template_name = 'duet_admin/create.html'
	form_class = EmployeeUpdateForm
	model=Employee
	cancel_url = 'duet_admin:employee-list'
	title = 'Edit -  '


class EmployeeDetail(DetailView):
	model = Employee
	template_name = 'duet_admin/employee/detail.html'
	context_object_name = 'employee'
	
class EmployeeDelete(DeleteView):
	model = Employee
	success_url = reverse_lazy('duet_admin:employee-list')
	template_name = 'duet_admin/confirm_delete.html'


####################################### Department ##############################################################

class DepartmentList(AddTableMixin, PageFilteredTableView):
	model = Department
	template_name = 'duet_admin/list.html'

	exclude=['id', 'description']
	filter_fields = {
		'name' : ['icontains'],
		'type' : ['exact'],
	}

	actions = [
		{'url' : 'duet_admin:department-detail', 'icon' : 'glyphicon glyphicon-th-large', 'tooltip' : 'Detail'},
		{'url' : 'duet_admin:department-update', 'icon' : 'glyphicon glyphicon-pencil', 'tooltip' : 'Update'},
		{'url' : 'duet_admin:department-delete', 'icon' : 'glyphicon glyphicon-trash', 'tooltip' : 'Delete'},
	]

	title = 'Department List'

	add_link = [
		{ 'url' : 'duet_admin:department-create', 'icon' : 'glyphicon glyphicon-plus'}
		]



class DepartmentCreate(CustomCreateView):
	model = Department
	fields = ['name','code','acronym', 'description', 'type']
	template_name = 'duet_admin/create.html'
	cancel_url = 'duet_admin:department-list'
	title = 'Create New Department  '


class DepartmentUpdate(CustomUpdateView):
	model = Department
	fields = ['name','code','acronym', 'description', 'type']
	template_name = 'duet_admin/create.html'
	cancel_url = 'duet_admin:department-list'
	title = 'Edit -  '

class DepartmentDetail(DetailView):
	model = Department
	template_name = 'duet_admin/department/detail.html'
	context_object_name = 'department'
	
class DepartmentDelete(DeleteView):
	model = Department
	success_url = reverse_lazy('duet_admin:department-list')
	template_name = 'duet_admin/confirm_delete.html'

####################################### Designation ##############################################################


class DesignationList(AddTableMixin, PageFilteredTableView):
	model = Designation
	template_name = 'duet_admin/list.html'

	exclude=['id']
	filter_fields = {
		'name' : ['icontains'],
		'grade__employee_class' : ['exact'],
	}

	actions = [
		{'url' : 'duet_admin:designation-detail', 'icon' : 'glyphicon glyphicon-th-large', 'tooltip' : 'Detail'},
		{'url' : 'duet_admin:designation-update', 'icon' : 'glyphicon glyphicon-pencil', 'tooltip' : 'Update'},
		{'url' : 'duet_admin:designation-delete', 'icon' : 'glyphicon glyphicon-trash', 'tooltip' : 'Delete'},
	]

	title = 'Designation List'

	add_link = [
		{ 'url' : 'duet_admin:designation-create', 'icon' : 'glyphicon glyphicon-plus'}
		]


class DesignationCreate(CustomCreateView):
	model = Designation
	fields = ['name', 'description', 'grade']
	template_name = 'duet_admin/create.html'
	cancel_url = 'duet_admin:designation-list'
	title = 'Create New Designation'


class DesignationUpdate(CustomUpdateView):
	model = Designation
	fields = ['name', 'description', 'grade']
	template_name = 'duet_admin/create.html'
	cancel_url = 'duet_admin:designation-list'
	title = 'Edit -  '

class DesignationDetail(DetailView):
	model = Designation
	template_name = 'duet_admin/designation/detail.html'
	context_object_name = 'designation'
	
class DesignationDelete(DeleteView):
	model = Designation
	success_url = reverse_lazy('duet_admin:designation-list')
	template_name = 'duet_admin/confirm_delete.html'

####################################### Grade ###############################################

class GradeList(AddTableMixin, PageFilteredTableView):
	model = Grade
	template_name = 'duet_admin/list.html'

	exclude=['id']
	filter_fields = {
		'grade_no' : ['exact'],
	}

	actions = [
		{'url' : 'duet_admin:grade-detail', 'icon' : 'glyphicon glyphicon-th-large', 'tooltip' : 'Detail'},
		{'url' : 'duet_admin:grade-update', 'icon' : 'glyphicon glyphicon-pencil', 'tooltip' : 'Update'},
		{'url' : 'duet_admin:grade-delete', 'icon' : 'glyphicon glyphicon-trash', 'tooltip' : 'Delete'},
	]

	title = 'Grade List'

	add_link = [
		{ 'url' : 'duet_admin:grade-create', 'icon' : 'glyphicon glyphicon-plus'}
		]


class GradeCreate(CustomCreateView):
	model = Grade
	fields = ['grade_no', 'description', 'employee_class']
	template_name = 'duet_admin/create.html'
	cancel_url = 'duet_admin:grade-list'
	title = 'Create New Designation'


class GradeUpdate(CustomUpdateView):
	model = Grade
	fields = ['grade_no', 'description', 'employee_class']
	template_name = 'duet_admin/create.html'
	cancel_url = 'duet_admin:grade-list'
	title = 'Edit -  '

class GradeDetail(DetailView):
	model = Grade
	template_name = 'duet_admin/grade/detail.html'
	context_object_name = 'grade'
	
class GradeDelete(DeleteView):
	model = Grade
	success_url = reverse_lazy('duet_admin:grade-list')
	template_name = 'duet_admin/confirm_delete.html'

####################################### Employee Class ######################################################################

class EmployeeClassList(AddTableMixin, PageFilteredTableView):
	model = EmployeeClass
	template_name = 'duet_admin/list.html'

	exclude=['id']
	filter_fields = {
		'name' : ['icontains'],
	}

	actions = [
		{'url' : 'duet_admin:employee-class-detail', 'icon' : 'glyphicon glyphicon-th-large', 'tooltip' : 'Detail'},
		{'url' : 'duet_admin:employee-class-update', 'icon' : 'glyphicon glyphicon-pencil', 'tooltip' : 'Update'},
		{'url' : 'duet_admin:employee-class-delete', 'icon' : 'glyphicon glyphicon-trash', 'tooltip' : 'Delete'},
	]

	title = 'Employee Class List'

	add_link = [
		{ 'url' : 'duet_admin:employee-class-create', 'icon' : 'glyphicon glyphicon-plus'}
		]


class EmployeeClassCreate(CustomCreateView):
	model = EmployeeClass
	fields = ['name', 'description']
	template_name = 'duet_admin/create.html'
	cancel_url = 'duet_admin:employee-class-list'
	title = 'Create New Employee Class'


class EmployeeClassUpdate(CustomUpdateView):
	model = EmployeeClass
	fields = ['name', 'description']
	template_name = 'duet_admin/create.html'
	cancel_url = 'duet_admin:employee-class-list'
	title = 'Edit -  '

class EmployeeClassDetail(DetailView):
	model = EmployeeClass
	template_name = 'duet_admin/employeeClass/detail.html'
	context_object_name = 'employeeClass'
	
class EmployeeClassDelete(DeleteView):
	model = EmployeeClass
	success_url = reverse_lazy('duet_admin:employee-class-list')
	template_name = 'duet_admin/confirm_delete.html'