from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.
class ProvidentFundProfile(models.Model):
	employee = models.OneToOneField('employee.Employee', on_delete=models.PROTECT)
	has_interest = models.BooleanField(verbose_name="Interest Taken")
	percentage = models.IntegerField(verbose_name='Percentage', default = 0)
	credit = models.FloatField(verbose_name= 'Credit', default = 0)

	def get_absolute_url(self):
		return reverse('account:provident-fund-list')

	def __str__(self):
		return self.employee.name

class MonthlyLogForGPF(models.Model):
	subscription = models.FloatField(verbose_name= 'Subscription', default = 0)
	interest = models.FloatField(verbose_name= 'Interest', default = 0)
	date = models.DateField(verbose_name = 'Month Ending')
	comment = models.TextField(null = True, blank = True, verbose_name= 'Comment')

	provident_fund_profile = models.ForeignKey('ProvidentFundProfile', verbose_name='Employee', on_delete= models.PROTECT)
	created_at = models.DateField(auto_now_add = True, auto_now = False, verbose_name="Created At")
	modified_at = models.DateField(auto_now = True, verbose_name="Modified At")

	def get_absolute_url(self):
		return reverse('account:provident-fund-monthly-logs')

	def __str__(self):
		return self.provident_fund_profile + self.date