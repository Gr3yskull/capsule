# Started on 27-Mar-2013; 9:25 AM, by mitthu
# The -( capsule )- project
# This file defines the query building against the models.

from models import Datasheet, Tag
from django.db.models import Q

class DatasheetQuery(object):
	def userIs(self, query): # User is a 'user object'
		self.query = self.query.filter(user=query)

	def urlIs(self, query):
		self.query = self.query.filter(url__iexact=unicode(query))
	# timstamp
	def kindIs(self, query):
		self.query = self.query.filter(kind__iexact=unicode(query))
	
	def titleStartsWith(self, query):
		self.query = self.query.filter(title__istartswith=unicode(query))
	def titleContains(self, query):
		self.query = self.query.filter(title__icontains=unicode(query))
	def descriptionContains(self, query):
		self.query = self.query.filter(description__icontains=unicode(query))
	def contentContains(self, query):
		self.query = self.query.filter(content__icontains=unicode(query))
	def taggedAs(self, query): # Case Sensitive
		self.query = self.query.filter(tags__iexact=unicode(query))
	def colourIs(self, query):
		self.query = self.query.filter(colour__iexact=unicode(query))

	def search(self, query):
		self.query = self.query.filter(	Q(title__icontains=unicode(query)) |
										Q(description__icontains=unicode(query)) |
										Q(content__icontains=unicode(query)) |
										Q(tags__iexact=unicode(query)))

	def result(self):
		return self.query

	def __init__(self, user=None):
		super(DatasheetQuery, self).__init__()
		self.user = user
		if user:
			self.query = Datasheet.objects.filter(user=self.user)
		else:
			self.query = Datasheet.objects.all()
