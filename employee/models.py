from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager

from duet_admin.choices import DEPARTMENT_TYPE, GENDER, EMPLOYEE_CATEGORY


class Department(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name')
    code = models.CharField(max_length=10, verbose_name='Code')
    acronym = models.CharField(max_length = 10, null = True, verbose_name = 'Acronym')
    description = models.TextField(null=True, blank = True, verbose_name='Description')
    type = models.CharField(max_length=2, choices=DEPARTMENT_TYPE, verbose_name = 'Type')
    created_at = models.DateField(auto_now_add = True, auto_now = False, verbose_name="Created At")
    modified_at = models.DateField(auto_now = True, verbose_name="Modified At") 

    def __str__(self):
        return self.acronym

    def get_absolute_url(self):
        return reverse('duet_admin:department-list')


class Designation(models.Model):
    name = models.CharField(max_length=200, verbose_name = 'Name')
    description = models.TextField(null=True, blank = True, verbose_name = 'Description')
    grade = models.ForeignKey('account.Grade', null = True, verbose_name = 'Grade', on_delete=models.PROTECT)

    created_at = models.DateField(auto_now_add = True, auto_now = False, verbose_name="Created At")
    modified_at = models.DateField(auto_now = True, verbose_name="Modified At") 

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('duet_admin:designation-list')


class Increment(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateField(auto_now_add = True, auto_now = False, verbose_name="Created At")
    modified_at = models.DateField(auto_now = True, verbose_name="Modified At") 


class Employee(AbstractBaseUser):
    name = models.CharField(verbose_name = 'Name', max_length=30)
    email = models.EmailField(verbose_name='Email', unique=True)
    address = models.TextField(blank=True, null = True, verbose_name = 'Address')
    tax_id_number = models.CharField(max_length=20, null = True, verbose_name = 'Tax ID')
    account_number = models.CharField(max_length=20, null = True, verbose_name= 'Account Number')
    joining_date = models.DateField(null = True, verbose_name="Joining Date")

    gender = models.CharField(max_length=1, choices=GENDER, default='m', verbose_name="Gender")
    category = models.CharField(max_length = 1, choices = EMPLOYEE_CATEGORY, verbose_name='Category', default = 't')
    dob = models.DateField(verbose_name = 'Date of Birth')
    image = models.FileField(upload_to='photos', null = True, blank= True)
    contact = models.CharField(verbose_name='Contact', max_length = 20, null= True, blank= True)

    created_at = models.DateField(auto_now_add = True, auto_now = False, verbose_name="Created At")
    modified_at = models.DateField(auto_now = True, verbose_name="Modified At") 

    designation = models.ForeignKey(Designation, verbose_name='Designation', on_delete=models.PROTECT)
    department = models.ForeignKey(Department, verbose_name='Department', on_delete=models.PROTECT)
    allowance_deductions = models.ManyToManyField('account.AllowanceDeduction', through='account.EmployeeAllowanceDeduction')
    increments = models.ManyToManyField(Increment, through='EmployeeIncrement')

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def _get_employee_class(self):
        return self.designation.grade.employee_class;

    employee_class = property(_get_employee_class)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('duet_admin:employee-list')

class WorkHistory(models.Model):
    joining_date = models.DateField()
    resigning_date = models.DateField(null = True)
    is_active = models.BooleanField()
    comment = models.TextField(null = True)
    designation = models.ForeignKey(Designation)
    employee = models.ForeignKey(Employee)
    created_at = models.DateField(auto_now_add = True, auto_now = False, verbose_name="Created At")
    modified_at = models.DateField(auto_now = True, verbose_name="Modified At") 


class EmployeeIncrement(models.Model):
    date = models.DateField()
    comment = models.TextField(null = True, blank = True)
    created_at = models.DateField(auto_now_add = True, auto_now = False, verbose_name="Created At")
    modified_at = models.DateField(auto_now = True, verbose_name="Modified At") 

    employee = models.ForeignKey(Employee)
    increment = models.ForeignKey(Increment)

