# Started on 31-Mar-2013; 9:20 PM, by mitthu
# The -( capsule )- project
# This file defines the data entry in models.

from models import Datasheet, Tag, ADDITIONAL_TYPES, COLOUR_CODES, lookup_in_tuple
from library.log import log
from datetime import datetime

class TagContol(object):
	def __tagGet(self, tag):
		try:
			return Tag.objects.filter(user__exact=self.user, tag__exact=unicode(tag))[0]
		except:
			return Tag(user=self.user, tag=unicode(tag), frequency=0)

	def tagIncrement(self, tag):
		t = self.__tagGet(tag)
		t.frequency += 1;
		t.save();
		return

	def tagDecrement(self, tag):
		t = self.__tagGet(tag)
		t.frequency -= 1;
		t.save();
		if t.frequency <= 0:
			t.delete()
			return
		return

	"""TagContol"""
	def __init__(self, user):
		super(TagContol, self).__init__()
		self.user = user

	def __unicode__(self):
		return u'For user: %s' % (self.user)

	def __str__(self):
		return 'For user: %s' % (self.user)

"""
Pending unit testing.
"""
class DatasheetControl(object):
	"""
	Imput/s
	-------
	- _id (string)

	Output/s
	--------
	- Success (Boolean)

	Improvements
	------------
	"""
	@staticmethod
	def delete(user, d_id):
		try:
			d = Datasheet.objects.get(user=user, id=d_id)
			# Updating tag structures
			tc = TagContol(user)
			# Decrement old tags (Tag Model)
			if d.tags:
				[tc.tagDecrement(tag) for tag in d.tags]
			d.delete()
			return True
		except:
			log.error('Failed to delete datasheet (%s) for user: %s' % (d_id, user))
		return False

	"""
	Imputs
	------
	- Tags (List)

	Improvements
	------------
	"""
	@staticmethod
	def add(user, url, title,
			timestamp   = None,
			kind        = None,
			description = None,
			content     = None,
			tags        = None,
			colour      = None):
		d = Datasheet(user=user, url=url, title=unicode(title))
		d.description = unicode(description)
		d.content     = unicode(content)
		
		if timestamp:
			d.timestamp = timestamp
		if tags:
			d.tags = [unicode(tag) for tag in tags]
		if lookup_in_tuple(ADDITIONAL_TYPES, kind):
			d.kind = unicode(kind)
		if lookup_in_tuple(COLOUR_CODES, colour):
			d.colour = colour
		try:
			log.info('Saving highlight %s' % d)
			d.save()
		except:
			log.error('Failed to save highlight for user: %s' % user)

		# Updating the tag structures
		if tags:
			tc = TagContol(user)
			[tc.tagIncrement(tag) for tag in d.tags]

	"""
	Imputs
	------
	
	Improvements
	------------
	- Ability to change the user
	- Handle exceptions
	"""
	@staticmethod
	def modify(user,
			d_id,
			url         = None,
			title       = None,
			kind        = None,
			description = None,
			content     = None,
			tags        = None,
			colour      = None):
		try:
			d = Datasheet.objects.get(id=d_id)
		except:
			return
		
		if url:
			d.url = unicode(url)
		if title:
			d.title = unicode(title)
		if lookup_in_tuple(ADDITIONAL_TYPES, kind):
			d.kind = unicode(kind)
		
		# The following can be empty
		d.description = unicode(description)		
		d.content = unicode(content)

		# Updating tag structures
		tc = TagContol(user)
		# Decrement old tags (Tag Model)
		if d.tags:
			[tc.tagDecrement(tag) for tag in d.tags]
		# Updating to new tags (Webpage Model)
		if tags:
			d.tags = [unicode(tag) for tag in tags]
		else:
			d.tags = None
		# Increment new tags (Tag Model)
		if tags:
			[tc.tagIncrement(tag) for tag in tags]

		try:
			d.save()
		except:
			log.error('Failed to modify highlight for user: %s' % user)

	def __init__(self):
		super(WebpageControl, self).__init__()
