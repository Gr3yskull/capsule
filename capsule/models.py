# Started on 26-Mar-2013; 5:00 PM, by mitthu
# The -( capsule )- project

from django.db import models
from django.core.urlresolvers import reverse
from djangotoolbox.fields import ListField
from djangotoolbox.fields import EmbeddedModelField
from django.contrib.auth.models import User
from datetime import datetime

# Globals
ADDITIONAL_TYPES = (
		('H', 'Highlight'),
		('S', 'Stackup'),
		('I', 'Image'),
	)
COLOUR_CODES = (
		("Blue"  , "#6EAAF5"),
		("Green" , "#7BBD3F"),
		("Yellow", "#FFBA01"),
		("Red"   , "#FF9C9C"),
	)
# COLOUR_CODES = (
# 		("White" , "#FFFFFF"),
# 		("Red"   , "#CC0000"),
# 		("Gray"  , "#C3C3C3"),
# 		("Green" , "#33CC33"),
# 		("Purple", "#CC0099"),
# 		("Yellow", "#FFCC00"),
# 		("Blue"  , "#3366FF"),
# 	)

def lookup_in_tuple(the_tuple, for_key):
	for t in the_tuple:
		if t[0] == for_key:
			return t[1]
	return None

"""
Explicitly the following need to be mentioned -
- user
- url
- title
"""
class Datasheet(models.Model):
	user        = models.ForeignKey(User)
	
	url         = models.URLField(null=False, blank=False, db_index=True)
	timestamp   = models.DateTimeField(default=datetime.now(), null=False, blank=False, db_index=True)
	kind        = models.CharField(max_length=1, choices=ADDITIONAL_TYPES, null=False, blank=False, default="H")
	
	title       = models.CharField(max_length=512, null=False, blank=False, db_index=True)
	description = models.CharField(max_length=2048, null=True, blank=False, db_index=True)
	content     = models.TextField(null=True, blank=False, db_index=True)
	tags        = ListField(models.CharField(max_length=40, null=False, blank=False), null=True, db_index=True)
	colour      = models.CharField(max_length=10, choices=COLOUR_CODES, null=True, blank=False)

	def serialize_to_json(self, url=False):
		h = {'id': self.id}
		
		if self.url:
			h['url'] 		= self.url
		
		if self.timestamp:
			h['timestamp'] 	= str(self.timestamp)
		if self.kind:
			h['kind'] 		= self.kind
		
		if self.title:
			h['title'] 		= self.title
		if self.description:
			h['description']= self.description
		if self.content:
			h['content'] 	= self.content
		if self.tags:
			h['tags'] 		= self.tags
		if self.colour:
			h['colour'] 	= self.colour
		return h

	def __unicode__(self):
		return unicode('Type: ' + self.kind + ', Title:'+ self.title)
		
	def get_kind(self):
		return lookup_in_tuple(ADDITIONAL_TYPES, self.kind)

	def get_colour(self):
		return lookup_in_tuple(COLOUR_CODES, self.colour)
	def get_colour_tuple(self):
		return (self.colour, lookup_in_tuple(COLOUR_CODES, self.colour))

	class Meta:
		ordering = ['-timestamp']

# Secondary structure for fast tag access
class Tag(models.Model):
	user      = models.ForeignKey(User, db_index=True)
	tag       = models.CharField(max_length=40, db_index=True, null=False, blank=False)
	frequency = models.BigIntegerField(null=False)
	# kind      = models.CharField(max_length=1, choices=ADDITIONAL_TYPES, default='H', null=False, blank=False)

	# def get_kind(self):
	# 	return lookup_in_tuple(ADDITIONAL_TYPES, self.kind)

	def __unicode__(self):
		return unicode(self.tag)

	def serialize_to_json(self):
		return {u'tag': self.tag, u'frequency': self.frequency}

	class Meta:
		ordering = ['-frequency']
