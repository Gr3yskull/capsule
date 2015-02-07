# Started on 31-Mar-2013; 8:32 PM, by mitthu
# The -( capsule )- project

from django.db import models
from django.core.urlresolvers import reverse
from djangotoolbox.fields import ListField
from djangotoolbox.fields import EmbeddedModelField
from django.contrib.auth.models import User
from datetime import datetime

# 31-March-2013
class Datasheet_v1(models.Model):
	user        = models.ForeignKey(User)
	
	url         = models.URLField(db_index=True, null=False, blank=False)
	timestamp   = models.DateTimeField(default=datetime.now(), null=False, blank=False, db_index=True)
	kind        = models.CharField(max_length=1, choices=ADDITIONAL_TYPES, null=False, blank=False, default="H")
	
	title       = models.CharField(max_length=512, null=False, blank=False, db_index=True)
	description = models.CharField(max_length=2048, null=True, blank=False, db_index=True)
	content     = models.TextField(null=True, blank=False, db_index=True)
	tags        = ListField(models.CharField(max_length=40, null=False, blank=False), null=True, db_index=True)
	colour      = models.CharField(max_length=10, choices=COLOUR_CODES, null=True, blank=False)

	def get_kind(self):
		for kind in ADDITIONAL_TYPES:
			if kind[0] == self.kind:
				return kind[1]
		return None

	def get_colour(self):
		for colour in COLOUR_CODES:
			if colour[0] == self.colour:
				return colour[1]
		return None

	def serialize_to_json(self, url=False):
		h = {}
		if url:
			h['url'] = self.url
		
		if self.timestamp:
			h['timestamp'] = self.timestamp
		if self.kind:
			h['kind'] = self.get_kind()
		if self.title:

			h['title'] = self.title
		if self.description:
			h['desc'] = self.description
		if self.content:
			h['content'] = self.content
		if self.tags:
			h['tags'] = self.tags
		if self.colour:
			h['colour'] = self.get_colour()
		return h

	def __unicode__(self):
		return unicode('Type: ' + self.kind + ', Title:'+ self.title)
		
	class Meta:
		ordering = ['timestamp']

# Secondary structure for fast tag access
# 31-March-2013
class Tag_v1(models.Model):
	user      = models.ForeignKey(User, db_index=True)
	tag       = models.CharField(max_length=40, db_index=True, null=False, blank=False)
	frequency = models.BigIntegerField(null=False)

	def __unicode__(self):
		return unicode(self.tag)
