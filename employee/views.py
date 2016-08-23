from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from duet_admin.utils import PageFilteredTableView, AddTableMixin
from .models import Employee


class EmployeeUpdate(UpdateView):
	model = Employee
	fields = ['address', 'contact', 'tax_id_number', 'account_number']
	template_name = 'employee/create.html'

	def get_success_url(self):
		return reverse_lazy('employees:employee-profile', args = (self.object.id,))

class EmployeeProfile(DetailView):
	model = Employee
	template_name = 'employee/employee/detail.html'
	context_object_name = 'employee'