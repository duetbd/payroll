from django import forms
from employee.models import Employee
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
			
class EmployeeCreateForm(forms.ModelForm):
	password = forms.CharField(
		widget=forms.PasswordInput,
		label= 'Password',
		required=True)
	confirm_password = forms.CharField(
		widget=forms.PasswordInput,
		label= 'Confirm password',
		required=True)
	class Meta:
		model = Employee
		fields = ['name', 'email', 'password', 'confirm_password' ,'address', 'gender', 'dob', 'joining_date', 'designation', 'department']
		widgets = {
            'dob': forms.DateInput(attrs={'class':'date-picker'}),
            'joining_date': forms.DateInput(attrs={'class':'date-picker'}),
        }

	def clean(self):
		if (self.cleaned_data.get('password') != self.cleaned_data.get('confirm_password')):
			raise ValidationError("Passwords must match.")
		return self.cleaned_data


class EmployeeUpdateForm(forms.ModelForm):
	class Meta:
		model = Employee
		fields = ['name', 'email' ,'address', 'gender', 'dob', 'designation', 'department']