from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^allowanceDeductions/$', AllowanceDeductionList.as_view(), name = 'allowancededuction-list'),
    url(r'^allowanceDeductions/create/$', AllowanceDeductionCreate.as_view(), name = 'allowancededuction-create'),
    url(r'^allowanceDeductions/(?P<pk>\d+)/$', AllowanceDeductionDetail.as_view(), name = 'allowancededuction-detail'),
    url(r'^allowanceDeductions/update/(?P<pk>\d+)/$', AllowanceDeductionUpdate.as_view(), name = 'allowancededuction-update'),
    url(r'^allowanceDeductions/delete/(?P<pk>\d+)/$', AllowanceDeductionDelete.as_view(), name = 'allowancededuction-delete'),
  
    url(r'^departments/$', DepartmentList.as_view(), name = 'department-list'),
    url(r'^departments/create/$', DepartmentCreate.as_view(), name = 'department-create'),
    url(r'^departments/(?P<pk>\d+)/$', DepartmentDetail.as_view(), name = 'department-detail'),
    url(r'^departments/update/(?P<pk>\d+)/$', DepartmentUpdate.as_view(), name = 'department-update'),
    url(r'^departments/delete/(?P<pk>\d+)/$', DepartmentDelete.as_view(), name = 'department-delete'),

    url(r'^designations/$', DesignationList.as_view(), name = 'designation-list'),
    url(r'^designations/create/$', DesignationCreate.as_view(), name = 'designation-create'),
    url(r'^designations/(?P<pk>\d+)/$', DesignationDetail.as_view(), name = 'designation-detail'),
    url(r'^designations/update/(?P<pk>\d+)/$', DesignationUpdate.as_view(), name = 'designation-update'),
    url(r'^designations/delete/(?P<pk>\d+)/$', DesignationDelete.as_view(), name = 'designation-delete'),

    url(r'^employees/create/$', EmployeeCreate.as_view(), name = 'employee-create'),
    url(r'^employees/$', EmployeeList.as_view(), name = 'employee-list'),
    url(r'^employees/(?P<pk>\d+)/$', EmployeeDetail.as_view(), name = 'employee-detail'),
    url(r'^employees/update/(?P<pk>\d+)/$', EmployeeUpdate.as_view(), name = 'employee-update'),
    url(r'^employees/delete/(?P<pk>\d+)/$', EmployeeDelete.as_view(), name = 'employee-delete'), 

    url(r'^grades/create/$', GradeCreate.as_view(), name = 'grade-create'),
    url(r'^grades/$', GradeList.as_view(), name = 'grade-list'),
    url(r'^grades/(?P<pk>\d+)/$', GradeDetail.as_view(), name = 'grade-detail'),
    url(r'^grades/update/(?P<pk>\d+)/$', GradeUpdate.as_view(), name = 'grade-update'),
    url(r'^grades/delete/(?P<pk>\d+)/$', GradeDelete.as_view(), name = 'grade-delete'), 

    url(r'^employeeClasses/create/$', EmployeeClassCreate.as_view(), name = 'employee-class-create'),
    url(r'^employeeClasses/$', EmployeeClassList.as_view(), name = 'employee-class-list'),
    url(r'^employeeClasses/(?P<pk>\d+)/$', EmployeeClassDetail.as_view(), name = 'employee-class-detail'),
    url(r'^employeeClasses/update/(?P<pk>\d+)/$', EmployeeClassUpdate.as_view(), name = 'employee-class-update'),
    url(r'^employeeClasses/delete/(?P<pk>\d+)/$', EmployeeClassDelete.as_view(), name = 'employee-class-delete'), 
]