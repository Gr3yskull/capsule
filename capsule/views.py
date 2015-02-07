# Started on 27-Mar-2013; 5:27 PM, by mitthu
# The -( capsule )- project

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Template, RequestContext
from django.contrib.auth.decorators import login_required
import json

from models import Datasheet, Tag, ADDITIONAL_TYPES
from query import DatasheetQuery
from control import DatasheetControl
import forms

from library.response.jsonapi import *
from library.log import log

def homepage(request):
	return render_to_response('capsule-homepage.html', {}, RequestContext(request))

"""
page() view: Returns pages after appropriate filetering.

Input JSON keys
- kind

Returns
- requested_page_number (integer)
- total_pages (integer)
- rolls
- total_records (Total number of results)
- total_records_this
+ Standard Response


Improvement
-----------
- Prepare unit tests.
- Wrap standard response.
"""
@login_required
def page(request, page_number=0):
	context = 'page'
	(valid, cleaned_data, response) = prepare_status_for(request, context, forms.PageForm)

	if valid:
		# If 'page_number' is Null/empty string, then make it '0'
		if not page_number:
			page_number = 0;
		# Converting 'page_number' to an integer
		try:
			page_number = int(page_number)
		except ValueError:
			response['success'] = False
			response['errors'][context] = u'Not a valid page number.'
			return http_wrap_json(response)

		# Adding 'page_number' to the response
		response['requested_page_number'] = page_number

		start_from = page_number * 20
		end_at     = start_from + 20
		q          = DatasheetQuery(request.user)
		q.kindIs(cleaned_data['kind'])
		result     = q.result()[start_from:end_at]
		
		response['rolls'] = [ds.serialize_to_json() for ds in result]
		response['total_records'] = q.result().count()
		response['total_records_this'] = len(result)
		
		# Calculating total pages
		response['total_pages'] = response['total_records'] / 20 - 1;
		if response['total_records'] % 20:
			response['total_pages'] += 1
		if not response['total_records']:
			response['total_pages'] = 0

		response['success'] = True

	return http_wrap_json(response)

"""
modify() view: Modify a datasheet.

Input JSON keys
- _id
- url
- kind
- title
- description
- content
- tags
- colour

Returns
+ Standard Response


Improvement
-----------
- Prepare unit tests.
- Wrap standard response.
"""
@login_required
def modify(request, page_number=0):
	context = 'modify'
	(valid, cleaned_data, response) = prepare_status_for(request, context, forms.EditForm)
	log.info("Modification request for: %s" % request.raw_post_data);

	if valid:
		log.info("Modification request received: %s" % cleaned_data)
		DatasheetControl.modify(user=request.user,
			d_id    = cleaned_data['_id'],
			url    = cleaned_data['url'],
			kind   = cleaned_data['kind'],
			title  = cleaned_data['title'],
			description  = cleaned_data['description'],
			content  = cleaned_data['content'],
			colour = cleaned_data['colour'],
			tags   = cleaned_data['tags'])
		response['success'] = True
		response['roll'] = Datasheet.objects.get(id=cleaned_data['_id']).serialize_to_json()
	else:
		response['errors'][context] = "Failed to modify."
		response['success'] = False
	return http_wrap_json(response)

	return http_wrap_json(response)

"""
add() view: Add highlights

Input JSON keys
- url
- kind
- title
- description
- content
- tags
- colour

Returns
- requested_page_number (integer)
- total_pages (integer)
- rolls
- total_records (Total number of results)
- total_records_this
+ Standard Response


Improvement
-----------
- Prepare unit tests.
- Wrap standard response.
"""
@login_required
def add(request, page_number=0):
	context = 'add'
	(valid, cleaned_data, response) = prepare_status_for(request, context, forms.AddForm)

	if valid:
		log.info("Data Received: %s" % cleaned_data)
		DatasheetControl.add(user=request.user,
			url    = cleaned_data['url'],
			kind   = cleaned_data['kind'],
			title  = cleaned_data['title'],
			description  = cleaned_data['description'],
			content  = cleaned_data['content'],
			colour = cleaned_data['colour'],
			tags   = cleaned_data['tags'])
		response['success'] = True
	else:
		response['errors'][context] = "Failed to insert into the database."
		response['success'] = False
	return http_wrap_json(response)

"""
search() view: Returns pages after appropriate filetering.

Input JSON keys
- search (character field)
- kind

Returns
- requested_page_number (integer) (starts from 0)
- total_pages (integer) (starts from 1)
- rolls
- total_records (Total number of results) (starts from 1)
- total_records_this  (starts from 1)
+ Standard Response


Improvement
-----------
- Prepare unit tests.
- Wrap standard response.
"""
@login_required
def search(request, page_number=0):
	context = 'search'
	(valid, cleaned_data, response) = prepare_status_for(request, context, forms.SearchForm)

	if valid:
		# log.info("Searched for: %s" % request.raw_post_data)
		# If 'page_number' is Null/empty string, then make it '0'
		if not page_number:
			page_number = 0;
		# Converting 'page_number' to an integer
		try:
			page_number = int(page_number)
		except ValueError:
			response['success'] = False
			response['errors'][context] = u'Not a valid page number.'
			return http_wrap_json(response)

		# Adding 'page_number' to the response
		response['requested_page_number'] = page_number

		start_from  = page_number * 20
		end_at      = start_from + 20
		q           = DatasheetQuery(request.user)
		search_term = cleaned_data['search']
		q.search(search_term)
		# log.info("Search result: %s" % q.result())

		result     = q.result()[start_from:end_at]

		response['rolls'] = [ds.serialize_to_json() for ds in result]
		response['total_records'] = q.result().count()
		response['total_records_this'] = len(result)

		# Calculating total pages
		response['total_pages'] = response['total_records'] / 20 - 1;
		if response['total_records'] % 20:
			response['total_pages'] += 1
		if not response['total_records']:
			response['total_pages'] = 0
			
		# # Calculating total pages
		# response['total_pages'] = response['total_records'] / 20 - 1;
		# if response['total_pages'] > 0 and response['total_records'] % 20:
		# 	response['total_pages'] += 1
		# if not response['total_records']:
		# 	response['total_pages'] = 0

		# response['total_pages'] = 2
		response['success'] = True

	return http_wrap_json(response)

"""
delete() view: Deteles the appropriate datasheet.

Input JSON keys
- _id

Returns
+ Standard Response


Improvement
-----------
- Prepare unit tests.
"""
@login_required
def delete(request):
	context = 'delete'
	(valid, cleaned_data, response) = prepare_status_for(request, context, forms.DeleteForm)

	if valid:
		# if Datasheet.objects.get(id=cleaned_data['_id']):
		# 	DatasheetControl.modify(user=request.user, title="", tags = "")
		# 	DatasheetControl.delete(request.user, cleaned_data['_id'])
		# 	response['success'] = True
		# 	return http_wrap_json(response)
		if DatasheetControl.delete(request.user, cleaned_data['_id']):
			response['success'] = True
			return http_wrap_json(response)
		else:
			response['success'] = False
			response['errors'][context] = 'Such a datasheet does not exists.'
			return http_wrap_json(response)
	return http_wrap_json(response)

"""
tags_frequency() view: Returns tags for the tag cloud.

Input JSON keys
None

Returns
- total_tags
+ Standard Response

Improvement
-----------
- Prepare unit tests.
"""
@login_required
def tags_frequency(request):
	context = 'delete'
	response = get_default_response_status(context)

	tags = Tag.objects.filter(user=request.user)
	response['total_tags'] = tags.count()

	if response['total_tags']:
		response['tags'] = [t.serialize_to_json() for t in tags]
		# log.info("Tags serialized: %s" % response['tags'])
	else:
		response['tags'] = []
	
	response['success'] = True
	return http_wrap_json(response)


"""
Send content in table format.
- Deprecated
"""
# @login_required
# def page_html(request, page_number=0):
# 	response = """<tr>
# 		<td style="display:none">Wikipedia</td>
# 		<td>Wikipedia</td>
# 		<td>Some content</td>
# 		<td style="width:10%;display:none"><i class="icon-wrench"></i> <i class="icon-trash"></i> <i class="icon-share-alt"></i> <i class="icon-tasks"></i></td>
# 	</tr>"""
# 	return HttpResponse(response)

"""
misc_colour_codes() view: Returns the colour codes for named colours.
- Deprecated

Input JSON keys
- None

Returns
- colours (list)
	- [ {"hexcode": "CC0000", "name": "Red"}, ... ]
+ Standard Response

Improvement
-----------
- Prepare unit tests.
- Wrap standard response.
"""
# @login_required
# def misc_colour_codes(request):
# 	response = get_default_response_status('colour_codes', True)
# 	response['colours'] = list(Colour.objects.all().values())

# 	return http_wrap_json(response)
