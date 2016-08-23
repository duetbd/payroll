from django.conf.urls import url
from .views import *
from .allowanceDeductionManager import*
from .providentFund import*

urlpatterns = [
    url(r'^employees/manageAllowanceDeductions/(?P<pk>\d+)/$', ConfigureEmployeeAllowanceDeduction.as_view(), name = 'configure-employee-allowance-deduction'),
    url(r'^employees/(?P<pk>\d+)/$', AccountEmployeeDetail.as_view(), name = 'employee-detail'),
    url(r'^employees/$', EmployeeList.as_view(), name = 'employee-list'),
   	url(r'^employees/GenerateSalarySheet/(?P<pk>\d+)/$', SalarySheetCreate.as_view(), name = 'employee-salary-sheet'),

   	url(r'^salarySheets/$', SalarySheetList.as_view(), name = 'salary-sheet-list'),
   	url(r'^salarySheets/update/(?P<pk>\d+)/$', SalarySheetUpdate.as_view(), name = 'salary-sheet-update'),
   	url(r'^salarySheets/delete/(?P<pk>\d+)/$', SalarySheetDelete.as_view(), name = 'salary-sheet-delete'),
   	url(r'^salarySheets/detail/(?P<pk>\d+)/$', SalarySheetDetail.as_view(), name = 'salary-sheet-detail'),
    url(r'^salarySheets/freeze/(?P<pk>\d+)/$', SalarySheetConfirm.as_view(), name = 'salary-sheet-confirm'),

   	url(r'^allowanceDeductions$', AllowanceDeductionList.as_view(), name = 'allowance-deduction-list'),
    url(r'^allowanceDeductions/(?P<pk>\d+)/$', AllowanceDeductionDetail.as_view(), name = 'allowance-deduction-detail'),
   	url(r'^allowanceDeductions/edit/(?P<pk>\d+)/$', AllowanceDeductionUpdate.as_view(), name = 'allowance-deduction-update'),
   	url(r'^allowanceDeductions/ConfigureValuesForEmployeeClass/(?P<pk>\d+)/$', ConfigureAllowanceDeductionEmployeeClassValue.as_view(), name = 'configure-allowance-deduction-employee-class'),
   	url(r'^allowanceDeductions/ConfigureAllowancesDeductions$', ConfigureAllowanceDeduction.as_view(), name = 'configure-allowance-deduction'),

    url(r'^providentFunds$', ProvidentFundList.as_view(), name = 'provident-fund-list'),
    url(r'^providentFunds/create/$', ProvidentFundProfileCreate.as_view(), name = 'provident-fund-profile-create'),
    url(r'^providentFunds/edit/(?P<pk>\d+)/$', ProvidentFundProfileUpdate.as_view(), name = 'provident-fund-profile-update'),
    url(r'^providentFunds/detail/(?P<pk>\d+)/$', ProvidentFundProfileDetail.as_view(), name = 'provident-fund-profile-detail'),
    url(r'^providentFunds/delete/(?P<pk>\d+)/$', ProvidentFundProfileDelete.as_view(), name = 'provident-fund-profile-delete'),
    url(r'^providentFunds/generateMontlyLog/(?P<pk>\d+)/$', GenerateMonthlyLogForProvidentFund.as_view(), name = 'generate-provident-fund-monthly-log'),
    url(r'^montlyLogsForProvidentFunds$', ProvidentFundMonthlyLogList.as_view(), name = 'provident-fund-monthly-logs'),
]



