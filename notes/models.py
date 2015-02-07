# Started on 27-Jan-2013; 1:00 PM, by mitthu
# My Ambitious Project....

from django.db import models

class User(models.Model):
	username       = models.CharField(max_length=70)
	firstName      = models.CharField(max_length=70)
	lastName       = models.CharField(max_length=70)
	email          = models.EmailField()
	# passwordHash = models.CharField(max_length=)
	joinDate       = models.DateField()
	lastAccess     = models.DateField()
	# lastAccessIP = models.URLField()
	# address details
	# account details

	def __unicode__(self):
		return self.name
		
class UserSession(models.Model):
	user = models.ForeignKey(User)
	# All active sessions
	
	def __unicode__(self):
		return self.name

class Note(models.Model):
	user        = models.ForeignKey(User)
	title        = models.CharField(max_length=255)
	description = models.CharField(max_length=256)
	content     = models.TextField('content of note')
	website     = models.URLField()
	created_at = models.DateTimeField(auto_now_add=True, db_index=True)
	# tags

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['title']
