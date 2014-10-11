from django.db import models
from datetime import datetime


class Party(models.Model):
	name = models.CharField(max_length=128, unique=True)	
	def __unicode__(self):
		return self.name

class Constituency(models.Model):
	parent = models.ForeignKey('self', default=0)
	name = models.CharField(max_length=128, unique=True)

	def __unicode__(self):
		return self.name
	
class MSP(models.Model):
	foreignid = models.PositiveIntegerField(max_length=8, unique=True)
	constituency = models.ForeignKey(Constituency)
	party = models.ForeignKey(Party)
	firstname = models.CharField(max_length=128)
	lastname = models.CharField(max_length=128)

	def __unicode__(self):
		return self.name
