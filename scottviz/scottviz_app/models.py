from django.db import models
from datetime import datetime


class SPsession(models.Model):
	msps = models.ManyToManyField(MSP)
	session = models.IntegerField()
	startdate = models.DateField()
	enddate = models.DateField()
	def __unicode__(self):
		return self.name

class Constituency(models.Model):
	msps = models.ManyToManyField(MSP)
	name = models.CharField(max_length=128, unique=True)
	Type = models.BooleanField()
	regionname = models.CharField(max_length=128)
	def __unicode__(self):
		return self.name
	
class MSP(models.Model):
	spsession = models.ManyToManyField(SPsession)
	constituency = models.ManyToManyField(Constituency)
	divisions = models.ForeignKey(Division,unique=True)
	votes = models.ForeignKey(Vote,unique=True)
	party = models.ForeignKey(Party)
	firstname = models.CharField(max_length=128)
	lastname = models.CharField(max_length=128)
	job = models.CharField(max_length=128)
	def __unicode__(self):
		return self.name

class Party(models.Model):
	name = models.CharField(max_length=128)
	def __unicode__(self):
		return self.name

class Vote(models.Model):
	msps = models.ForeignKey(MSP,unique=True)
	divisions = models.ForeignKey(Division,unique=True)
	type = models.CharField(max_length=128)
	def __unicode__(self):
		return self.name

class Division(models.Model):
	msps = models.ForeignKey(MSP,unique=True)
	votes = models.ForeignKey(Vote,unique=True)
	date = models.DateField()
	number = models.IntegerField()
	link = models.URLField(max_length=128)
	agreement = models.BooleanField()
	question = models.TextField()
	motionid = models.CharField(max_length=12)
	motiontext = models.TextField()
	topic = models.CharField(max_length=30)
	def __unicode__(self):
		return self.name
