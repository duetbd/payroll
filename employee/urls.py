from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^profile/(?P<pk>\d+)/$', EmployeeProfile.as_view(), name = 'employee-profile'),
    url(r'^employees/edit/(?P<pk>\d+)/$', EmployeeUpdate.as_view(), name = 'employee-update'),
]
