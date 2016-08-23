from django.shortcuts import render, redirect
from django.views.generic import  DetailView, View
from django.core.urlresolvers import reverse_lazy

from django.views.generic import DetailView, DeleteView

from .forms import MonthlyProvidentFundForm

from provident_fund.models import ProvidentFundProfile, MonthlyLogForGPF
from .models import EmployeeAllowanceDeduction

from duet_admin.utils import PageFilteredTableView, AddTableMixin, CustomUpdateView, CustomCreateView

class ProvidentFundList(AddTableMixin, PageFilteredTableView):
	model = ProvidentFundProfile
	template_name = 'account/providentFund/list.html'

	exclude=['created_at', 'modified_at']

	filter_fields = {
		'employee' : ['exact'],
		'has_interest' : ['exact'],
	}

	add_link = [
		{ 'url' : 'account:provident-fund-profile-create', 'icon' : 'glyphicon glyphicon-plus'}
		]

	actions = [
		{'url' : 'account:provident-fund-profile-detail', 'icon' : 'glyphicon glyphicon-th-large', 'tooltip' : 'Detail'},
		{'url' : 'account:generate-provident-fund-monthly-log', 'icon' : 'glyphicon glyphicon-usd', 'tooltip' : 'Generate Monthly Log'},
		{'url' : 'account:provident-fund-profile-delete', 'icon' : 'glyphicon glyphicon-trash', 'tooltip' : 'Delete'},
	]

	title = 'General Provident Fund Profile List'


class ProvidentFundProfileCreate(CustomCreateView):
	model = ProvidentFundProfile
	fields = ['employee', 'has_interest','percentage']
	template_name = 'account/create.html'
	cancel_url = 'account:provident-fund-list'
	title = 'Add New Provident Fund Profile'

class ProvidentFundProfileUpdate(CustomUpdateView):
	model = ProvidentFundProfile
	fields = ['has_interest','percentage']
	template_name = 'account/create.html'
	cancel_url = 'account:provident-fund-list'
	title = 'Edit - '


class ProvidentFundProfileDelete(DeleteView):
	model = ProvidentFundProfile
	success_url = reverse_lazy( 'account:provident-fund-list')
	template_name = 'account/confirm_delete.html'

	def delete(self, request, *args, **kwargs):
		try:
			super().delete(request, *args, **kwargs)
			return redirect('account:provident-fund-list')
		except ProtectedError:
			return render(request, 'common/protection_error.html')


class ProvidentFundProfileDetail(DetailView):
	model = ProvidentFundProfile
	template_name = 'account/providentFund/profile/detail.html'
	context_object_name = 'providentFundProfile'


class GenerateMonthlyLogForProvidentFund(View):

	def get(self, request, pk):
		provident_fund_profile = ProvidentFundProfile.objects.select_related('employee').get(pk = pk)
		employee = provident_fund_profile.employee
		employee_allowance_deductions = EmployeeAllowanceDeduction.objects.fierlt(employee = employee)
		basic_pay = employee_allowance_deductions.get(allowance_deduction__code = 'ba')
		personal_pay = employee_allowance_deductions.get(allowance_deduction__code = 'pp')

		initial = dict()
		percentage = provident_fund_profile.percentage
		initial['subscription'] = (basic_pay.value + personal_pay.value) * (percentage/100)
		initial['interest'] = 0
		if provident_fund_profile.has_interest :
				initial['interest'] = provident_fund_profile.credit * .13
		form = MonthlyProvidentFundForm(provident_fund_profile = provident_fund_profile, initial =initial)

		return render(request, 'account/providentFund/monthlyLog.html', {'form' : form, 'employee' : employee, 'provident_fund_profile' : provident_fund_profile})

	def post(self, request, pk):
		provident_fund_profile = ProvidentFundProfile.objects.get(pk = pk)
		form = MonthlyProvidentFundForm(request.POST, provident_fund_profile = provident_fund_profile)
		
		if form.is_valid():
			form.save()
			return redirect('account:provident-fund-list')

class ProvidentFundMonthlyLogList(AddTableMixin, PageFilteredTableView):
	model = MonthlyLogForGPF
	template_name ='account/list.html'

	exclude=['created_at', 'modified_at']

	filter_fields = {
		'date' : ['exact'],
	}


	actions = [
		{'url' : 'account:employee-detail', 'icon' : 'glyphicon glyphicon-th-large', 'tooltip' : 'Detail'},
	]

	title = 'Montly Logs For General Provident'

class ProvidentFundManager(object):
	"""docstring for ProvidentFundManager"""
	def __init__(self, arg):
		super(ProvidentFundManager, self).__init__()
		self.arg = arg


