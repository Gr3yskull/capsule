# Started on 30-Mar-2013, by mitthu
# Initially a part of the 'authentication' app

import json
from library.log import *
from library.errors import *

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.models import User

def get_default_response_status(context, success=False):
	response = {}
	response[u'success'] = success
	response[u'context'] = context
	response[u'errors'] = {}
	response[u'errors'][context] = None
	return response

def prepare_status_for(request, context=u"default", form_name=None):
	context = unicode(context)
	response = get_default_response_status(context)
	
	valid = False
	parsed_json = {}
	# if request.is_ajax() and request.method == 'POST':
	# Done to resolve the problem of Extension
	if request.method == 'POST':
		try:
			parsed_json = json.loads(request.raw_post_data)
			valid = True
		except:
			log.error("Invalid json submitted to '%s': %s" % (request.path, request.raw_post_data))
			response['errors'][context] = ERR_INVALID_FORMAT
	else:
		response[u'errors'][context] = ERR_NOT_POST_OR_AJAX

	# Checking form validity
	if valid and form_name is not None:
		f = form_name(parsed_json)
		if f.is_valid():
			parsed_json = f.cleaned_data
		else:
			valid = False
			response[u'errors'][context] = ERR_INVALID_FORM_ENTRIES
			response['errors'] = dict(response['errors'].items() + f.errors.items())
	# If the request is valid upto this point, then properly formatted data is sent.
	# This makes the 'success' criteria of the response to be true.
	if valid:
		response[u'success'] = True
	return (valid, parsed_json, response)

def http_wrap_json(json_object):
	return HttpResponse(json.JSONEncoder().encode(json_object), content_type="application/json")
