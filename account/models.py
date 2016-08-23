from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from duet_admin.choices import PAYMENT_TYPE, ALLOWANCE_DEDUCTION_TYPE, EMPLOYEE_CLASS

class AllowanceDeduction(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name")
    description = models.TextField(null=True, blank = True, verbose_name="Description")
    code = models.CharField(max_length = 3, verbose_name = "Code", null = True)
  
    category = models.CharField(max_length=2, choices=ALLOWANCE_DEDUCTION_TYPE, verbose_name="Type")
    value = models.ManyToManyField('EmployeeClass', through='AllowanceDeductionEmployeeClassValue')
    is_percentage = models.BooleanField(verbose_name="Percentage")
    is_applicable = models.BooleanField(verbose_name="Applicable")
    payment_type = models.CharField(max_length=2, choices=PAYMENT_TYPE, default='m', verbose_name="Payment Type")
    order = models.IntegerField(null= True, blank = True, verbose_name='Order')

    created_at = models.DateField(auto_now_add = True, auto_now = False, verbose_name="Created At")
    modified_at = models.DateField(auto_now = True, verbose_name="Modified At")

    class Meta:
    	ordering = ['order']
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('duet_admin:allowancededuction-list')


class EmployeeAllowanceDeduction(models.Model):
    value = models.FloatField(null = True, blank = True)
    is_percentage = models.BooleanField()
    is_applicable = models.BooleanField()
    employee = models.ForeignKey('employee.Employee', on_delete=models.PROTECT)
    allowance_deduction = models.ForeignKey(AllowanceDeduction, on_delete=models.PROTECT)   

    created_at = models.DateField(auto_now_add = True, auto_now = False, verbose_name="Created At")
    modified_at = models.DateField(auto_now = True, verbose_name="Modified At") 

    def __str__(self):
        return self.allowance_deduction.name

    class Meta:
        unique_together = ("employee", "allowance_deduction")
        ordering = ['allowance_deduction__order']
            

class SalarySheet(models.Model):
    employee = models.ForeignKey('employee.Employee', verbose_name= 'Employee')
    date = models.DateField(verbose_name = 'Month Ending')
    is_freezed = models.BooleanField(default=False, verbose_name= 'Freezed')
    is_withdrawan = models.BooleanField(default = True, verbose_name='Withdrawn')

    allowance_deductions = models.ManyToManyField(AllowanceDeduction, through='SalarySheetDetails')

    
    comment = models.TextField(null = True, blank = True)
    created_at = models.DateField(auto_now_add = True, auto_now = False, verbose_name="Created At")
    modified_at = models.DateField(auto_now = True, verbose_name="Modified At") 

    #@property
    #def get_net_allowance(self):
    #    allowance = SalarySheet.objects.aggregate(sum('amount'))
    #    if allowance is None:
    #        allowance = 0
    #    return allowance
    
    #def get_net_deduction(self):
    #    deduction = SalarySheetDetails.objects.filter(salary_sheet = self).exclude(allowance_deduction__category = 'd').aggregate(total=Sum("amount"))
    #    if deduction is None:
    #         deduction = 0
    #    return deduction

    #net_allowance= property(get_net_allowance)
    #net_deduction = property(get_net_deduction)

    def __str__(self):
        return 'Salary Sheet-' + str(self.id)


class SalarySheetDetails(models.Model):
    salary_sheet = models.ForeignKey(SalarySheet, on_delete=models.CASCADE)
    allowance_deduction = models.ForeignKey(AllowanceDeduction, on_delete=models.PROTECT)
    amount = models.FloatField(default = 0)

    created_at = models.DateField(auto_now_add = True, auto_now = False, verbose_name="Created At")
    modified_at = models.DateField(auto_now = True, verbose_name="Modified At") 

    class Meta:
        ordering = ['allowance_deduction__order']

class EmployeeClass(models.Model):
    name = models.CharField(max_length= 50, verbose_name= 'Title')
    description = models.TextField(verbose_name = 'Description', null = True, blank = 'True')

    created_at = models.DateField(auto_now_add = True, auto_now = False, verbose_name="Created At")
    modified_at = models.DateField(auto_now = True, verbose_name="Modified At") 

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('duet_admin:employee-class-list')


class AllowanceDeductionEmployeeClassValue(models.Model):
    amount = models.FloatField()
    allowance_deduction = models.ForeignKey(AllowanceDeduction)
    employee_class = models.ForeignKey(EmployeeClass)

    class Meta:
        unique_together = ("employee_class", "allowance_deduction")
    

class Grade(models.Model):
    grade_no = models.IntegerField(verbose_name= 'Grade')
    description = models.TextField(verbose_name = 'Description', null = True, blank = 'True')
    employee_class = models.ForeignKey(EmployeeClass, verbose_name= 'Class')

    created_at = models.DateField(auto_now_add = True, auto_now = False, verbose_name="Created At")
    modified_at = models.DateField(auto_now = True, verbose_name="Modified At") 


    def __str__(self):
        return 'Grade-' + str(self.grade_no)

    def get_absolute_url(self):
        return reverse('duet_admin:grade-list')