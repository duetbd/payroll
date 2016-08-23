from django.forms.formsets import Form, BaseFormSet, formset_factory, ValidationError
from django import forms
from .models import EmployeeAllowanceDeduction, AllowanceDeduction, SalarySheetDetails, SalarySheet, AllowanceDeductionEmployeeClassValue
from employee.models import Employee
from provident_fund.models import MonthlyLogForGPF
from django.forms.models import modelformset_factory
from django.forms.models import BaseInlineFormSet

class SalarySheetDetailsEditForm(forms.ModelForm):
	amount = forms.IntegerField(label='')
	class Meta:
		model = SalarySheetDetails
		fields = ['amount', ]



class SalarySheetForm(forms.ModelForm):
	class Meta:
		model = SalarySheet
		fields = ['date', 'is_withdrawan']
		widgets = {"date" : forms.DateInput(attrs={'class':'month-picker'})} 


class SalarySheetDetailsForm(forms.ModelForm):
	amount = forms.IntegerField(label='')
	class Meta:
		model = SalarySheetDetails
		fields = ['amount', ]

	def __init__(self, *args, **kwargs):
		self.allowance_deduction = kwargs.pop('allowance_deduction')
		super().__init__(*args, **kwargs)

	def save(self, commit=True):
		instance = super(SalarySheetDetailsForm, self).save(commit=False)
		instance.allowance_deduction = self.allowance_deduction
		if commit:
			instance.save()
		return instance

class EmployeeAllowanceDeductionForm(forms.ModelForm):

	is_applicable = forms.BooleanField(label = "", required = False)
	is_percentage = forms.BooleanField(label = "", required = False)
	value = forms.IntegerField(label = "", required= False)
	class Meta:
		model = EmployeeAllowanceDeduction
		fields =['is_applicable', 'value', 'is_percentage']


	def __init__(self, *args, **kwargs):
		self.allowance_deduction = kwargs.pop('allowance_deduction')
		super(EmployeeAllowanceDeductionForm, self).__init__(*args, **kwargs)

	def save(self, commit=True):
		instance = super(EmployeeAllowanceDeductionForm, self).save(commit=False)
		instance.allowance_deduction = self.allowance_deduction
		if commit:
			instance.save()
		return instance
		

class AllowanceDeductionEmployeeClassValueForm(forms.ModelForm):

	class Meta:
		model = AllowanceDeductionEmployeeClassValue
		fields =['amount',]

	def __init__(self, *args, **kwargs):
		self.employee_class = kwargs.pop('employee_class')
		self.allowance_deduction = kwargs.pop('allowance_deduction')
		super().__init__(*args, **kwargs)

	def save(self, commit=True):
		instance = super().save(commit=False)
		instance.employee_class = self.employee_class
		instance.allowance_deduction = self.allowance_deduction
		if commit:
			instance.save()
		return instance

class ConfigureAllowanceDeductionForm (forms.ModelForm):
	is_applicable = forms.BooleanField(label = "", required = False)
	order = forms.IntegerField(label = "", required= False)
	class Meta:
		model = AllowanceDeduction
		fields = ['is_applicable', 'order']


class MonthlyProvidentFundForm(forms.ModelForm):
	class Meta:
		model = MonthlyLogForGPF
		fields = ['subscription', 'interest', 'date', 'comment']
		widgets = {"date" : forms.DateInput(attrs={'class':'month-picker'})} 

	def __init__(self, *args, **kwargs):
		self.provident_fund_profile = kwargs.pop('provident_fund_profile')
		super().__init__(*args, **kwargs)

	def save(self, commit=True):
		instance = super().save(commit=False)
		instance.provident_fund_profile = self.provident_fund_profile
		if commit:
			subscription = instance.subscription
			self.provident_fund_profile.credit = self.provident_fund_profile.credit + subscription
			self.provident_fund_profile.save()
			instance.save()
		return instance
			
