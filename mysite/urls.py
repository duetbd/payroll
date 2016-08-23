from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^duet_admin/', include('duet_admin.urls', namespace = 'duet_admin')),
    url(r'^account/', include('account.urls', namespace = 'account')),
    url(r'^employees/', include('employee.urls', namespace = 'employees')),
]

