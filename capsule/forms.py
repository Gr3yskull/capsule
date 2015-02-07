"""
Started on 7-Apr-2013; 7:35 PM, by mitthu
Part of the -( capsule )- project
"""

from django import forms
from models import ADDITIONAL_TYPES, lookup_in_tuple
from library.log import log

# Handle colours properly
class EditForm(forms.Form):
	# Actual max length = 24
	_id = forms.CharField(max_length=30, required=True)
	url         = forms.URLField(required=False)
	kind        = forms.CharField(max_length=1, required=False)
	
	title       = forms.CharField(max_length=512, required=False)
	description = forms.CharField(max_length=2048, required=False)
	content     = forms.CharField(max_length=10000, required=False)
	tags        = forms.CharField(max_length=1024, required=False)
	colour      = forms.CharField(max_length=10, required=False)

	def clean_kind(self):
		kind = self.cleaned_data['kind']
		if not kind:
			return None
		if not lookup_in_tuple(ADDITIONAL_TYPES, kind.upper()):
			raise forms.ValidationError("Unsupported datasheet kind requested.")
		return kind.upper()

	def clean_tags(self):
		tags = self.cleaned_data['tags']
		if not tags:
			return None
		tags_clean = tags.replace(', ', ',').replace(' ,', ',').replace(' , ', ',')
		if tags_clean[-1] == ',':
			tags_clean = tags_clean[:-1]
		tags_list = tags_clean.split(',')

		for tag in tags_list:
			log.info("Length of tag: %d" % tag.__len__());
			if tag.__len__() > 30:
				raise forms.ValidationError("Tag length cannot be greater than 30 characters.")
			if not tag:
				tags_list.remove(tag)
		
		return tags_list

# Handle colours properly
class AddForm(forms.Form):
	url         = forms.URLField(required=True)
	kind        = forms.CharField(max_length=1, initial="H")
	
	title       = forms.CharField(max_length=512, required=True)
	description = forms.CharField(max_length=2048, required=False)
	content     = forms.CharField(max_length=10000, required=False)
	tags        = forms.CharField(max_length=1024, required=False)
	colour      = forms.CharField(max_length=10, required=False)

	def clean_kind(self):
		kind = self.cleaned_data['kind']
		if not lookup_in_tuple(ADDITIONAL_TYPES, kind.upper()):
			raise forms.ValidationError("Unsupported datasheet kind requested.")
		return kind.upper()

	def clean_tags(self):
		tags = self.cleaned_data['tags']
		if not tags:
			return None
		tags_clean = tags.replace(', ', ',').replace(' ,', ',').replace(' , ', ',')
		if tags_clean[-1] == ',':
			tags_clean = tags_clean[:-1]

		tags_list = tags_clean.split(',')

		for tag in tags_list:
			log.info("Length of tag: %d" % tag.__len__());
			if tag.__len__() > 30:
				raise forms.ValidationError("Tag length cannot be greater than 30 characters.")
			if not tag:
				tags_list.remove(tag)
		
		return tags_list

class PageForm(forms.Form):
	kind = forms.CharField(max_length=1, initial="H", required=False)

	def clean_kind(self):
		kind = self.cleaned_data['kind']
		if not lookup_in_tuple(ADDITIONAL_TYPES, kind.upper()):
			raise forms.ValidationError("Unsupported datasheet kind requested.")
		return kind.upper()

class SearchForm(forms.Form):
	search = forms.CharField(max_length=40, required=True)
	
class DeleteForm(forms.Form):
	# Actual max length = 24
	_id = forms.CharField(max_length=30, required=True)
