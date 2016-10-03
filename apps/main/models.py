from __future__ import unicode_literals
from django.db import models

class Currency(models.Model):
	title = models.CharField(max_length=20,
							 verbose_name='Currency title',
							 unique=True)
	values = models.ManyToManyField('CurrencyValues',
									blank=True)

	def __unicode__(self):
		return self.title
	
	@property
	def currency_values(self):
		currency_values = self.values.all()
		cv_dict = dict()
		for cv in currency_values:
			cv_dict[cv.title] = cv.value
		return cv_dict
	

class CurrencyValues(models.Model):
	title = models.CharField(max_length=20,
							verbose_name='Currency values title')
	value = models.FloatField(verbose_name='Value')

	def __unicode__(self):
		return "%s:%s" % (self.title, self.value)