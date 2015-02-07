# Started on 26-Mar-2013; 5:00 PM, by mitthu
# The -( capsule )- project

from django.db import models
from django.core.urlresolvers import reverse
from djangotoolbox.fields import ListField
from djangotoolbox.fields import EmbeddedModelField
from django.contrib.auth.models import User
from datetime import datetime

# Deprecated on 31-March-2013, in favour of 'choices' field option.
class Colour(models.Model):
	name = models.CharField(max_length=10, primary_key=True, db_index=True)
	# The front '#' is truncated
	hexcode = models.CharField(max_length=6, null=False)

	def __unicode__(self):
		return unicode(self.name)

# Deprecated on 31-March-2013
class URLReference(models.Model):
	user = models.ForeignKey(User, db_index=True)
	url = models.URLField(db_index=True, null=False)
	is_stackup = models.BooleanField(default=False)
	# The tags in here are for the stackups
	tags = ListField(models.CharField(max_length=40), db_index=True)

	# Just extra metadata
	saved_on = models.DateTimeField(default=datetime.now(), db_index=True)

	def __unicode__(self):
		return u'(%s) %s' % (self.user, self.url)
	
	class Meta:
		ordering = ['saved_on']
	# Older implementation
	# userid = models.CharField(max_length=70, db_index=True)
	# data = ListField(EmbeddedModelField('Highlight'), db_index=True)
