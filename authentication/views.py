# Started on 26-Feb-2013; 3:37 PM, by mitthu

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Template, RequestContext

from django.contrib import auth
from django.contrib.auth.models import User
import json
from library.log import log
from library.response.jsonapi import *
from library.mailer import reset_password_for_user
import forms
import constants as c

def home(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/dashboard/")
	return render_to_response('authentication-index.html', {}, RequestContext(request))

# def get_default_response_status(context):
# 	response = {}
# 	response[u'success'] = False
# 	response[u'context'] = context
# 	response[u'errors'] = {}
# 	response[u'errors'][context] = None
# 	return response

# def prepare_status_for(request, context=u"default", form_name=None):
# 	context = unicode(context)
# 	response = get_default_response_status(context)
	
# 	valid = False
# 	parsed_json = {}
# 	if request.is_ajax() and request.method == 'POST':
# 		try:
# 			parsed_json = json.loads(request.raw_post_data)
# 			valid = True
# 		except:
# 			log.error("Invalid json submitted to '%s': %s" % (request.path, request.raw_post_data))
# 			response['errors'][context] = u'Posted data format is invalid.'
# 	else:
# 		response[u'errors'][context] = u"Method is not POST or request is not Ajax."

# 	# Checking form validity
# 	if valid and form_name is not None:
# 		f = form_name(parsed_json)
# 		if f.is_valid():
# 			parsed_json = f.cleaned_data
# 		else:
# 			valid = False
# 			response[u'errors'][context] = u"Failed due to invalid form entries."
# 			response['errors'] = dict(response['errors'].items() + f.errors.items())
# 	# If the request is valid upto this point, then properly formatted data is sent.
# 	# This makes the 'success' criteria of the response to be true.
# 	if valid:
# 		response[u'success'] = True
# 	return (valid, parsed_json, response)

# def http_wrap_json(json_object):
# 	return HttpResponse(json.dumps(json_object), content_type="application/json")

"""
Input JSON keys
- username
- password
- email
- first_name
- last_name

Returns
{
	'success': True
	'context': 'signup',
	'errors' : {
		'signup': '',
		...
	}
}
"""
def signup(request):
	context = u'signup'
	(valid, new_user, response) = prepare_status_for(request, context, forms.SignupForm)
	if valid:
		try:
			user = User.objects.get(username=new_user['username'])
			# If user already exists
			response['success'] = False
			response['errors'][context] = 'User already exists.'
		except User.DoesNotExist:
			# Creating a new user
			u = User()
			u.set_password(new_user['password'])
			u.username   = new_user['username']
			u.email      = new_user['email']			
			u.first_name = new_user['first_name']
			u.last_name  = new_user['last_name']
			try:
				u.save()
				response['success'] = True
				log.info("New user signup: %s" % (new_user['username']));
			except:
				log.error("Error saving new user: %s" % (new_user['username']));
				response['success'] = False
				response['errors'][context] = 'Error saving new user.'
	return http_wrap_json(response)

"""
Input JSON keys
- username
- email

Returns
+ Standard Response
"""
def reset_password(request):
	context = u'reset_password'
	(valid, cleaned_data, response) = prepare_status_for(request, context, forms.ResetPasswordForm)
	if valid:
		try:
			user = User.objects.get(username=cleaned_data['username'])
		except User.DoesNotExist:
			response['success'] = False
			response['errors'][context] = 'No such user exists.'
			return http_wrap_json(response)
		if user.email != cleaned_data['email']:
			response['success'] = False
			response['errors'][context] = 'The entered email address does not match with our records.'
			return http_wrap_json(response)
		reset_password_for_user(user)
		log.info("Reset Password serviced for: %s" % (cleaned_data['username']));
	return http_wrap_json(response)

"""
Modifications to the user profile are atomic in nature. Everything succeeds or everything fails.

Input JSON keys
- username: 'mitthu' (required)
- password: 'password' (required)
- new_username: 'mitthu'
- new_password: 'password'
- new_email
- new_first_name
- new_last_name
Returns
{
	'for_username': 'mitthu'.
	'success': True,
	'context': 'modify',
	'errors' : {
		'modify': '',
		...
	}
}

Improvement
-----------
- Add test cases for ERR_NOTHING_CHANGED (new_username cannot be blank).
"""
def modify(request):
	context=u'modify'
	(valid, user, response) = prepare_status_for(request, context, forms.ModifyUserForm)
	# To keep track of any changes
	changed = False
	if valid:
		u = auth.authenticate(username=user['username'], password=user['password'])
		if u is not None:
			# The following 'if' clauses prevent old data from being overwritten.
			if user['new_password']:
				changed = True
				u.set_password(user['new_password'])
			if user['new_username']:
				changed = True
				try:
					user = User.objects.get(username=user['new_username'])
					# If user already exists
					response['success'] = False
					response['errors'][context] = 'Username already exists.'
					return http_wrap_json(response)
				except User.DoesNotExist:
					u.username   = user['new_username']
			if user['new_email']:
				changed = True
				u.email      = user['new_email']
			if user['new_first_name']:
				changed = True
				u.first_name = user['new_first_name']
			if user['new_last_name']:
				changed = True
				u.last_name  = user['new_last_name']
			try:
				log.info("Saving modified user (old username): %s" % user['username'])
				u.save()
				response[u'success'] = True
			except:
				log.error("Failed to save modified user (old username): %s" % user['username'])
				response['success'] = False
				response['errors'][context] = u'Failed to modify user details.'
		else:
			response['success'] = False
			response['errors'][context] = c.ERR_CREDNTIALS
		if not changed:
			response['success'] = False
			response['errors'][context] = c.ERR_NOTHING_CHANGED
	return http_wrap_json(response)

"""
Input JSON keys
- username: 'mitthu'

Returns
{
	'for_username': 'mitthu'.
	'success': True,
	'context': 'username_available',
	'errors' : {
		'username_available': '',
		...
	}
}
"""
def username_available(request):
	context=u'username_available'
	(valid, user, response) = prepare_status_for(request, context, forms.UserAvailabilityForm)
	if valid:
		user = user[u'username']
		response[u'for_username'] = user
		log.info(u"Checking user availability: %s" % user)
		try:
			user = User.objects.get(username=user)
			# If user already exists
			response[u'success'] = False
			response['errors'][context] = u'User already exists.'
		except User.DoesNotExist:
			response[u'success'] = True
	return http_wrap_json(response)

"""
Input JSON keys
- username: 'mitthu'
- password: 'password'

Returns
{
	'for_username': 'mitthu'.
	'success': True,
	'context': 'delete_account',
	'errors' : {
		'delete_account': '',
		...
	}
}

Improvement
-----------
- Delete all user data.
"""
def delete_account(request):
	context=u'delete_account'
	(valid, user, response) = prepare_status_for(request, context, forms.DeleteAccountForm)
	if valid:
		u = auth.authenticate(username=user['username'], password=user['password'])
		if u is not None:
			try:
				log.info("Deleting user: %s" % user['username'])
				u.delete()
				response[u'success'] = True
			except:
				log.error("Failed to delete user: %s" % user['username'])
				response['success'] = False
				response['errors'][context] = c.ERR_CREDNTIALS			
		else:
			response['success'] = False
			response['errors'][context] = c.ERR_CREDNTIALS
	return http_wrap_json(response)

"""
login() view. Made for use with the web-app.

Input JSON keys
- username: 'mitthu'
- password: 'password'

Returns
{
	'for_username': 'mitthu'.
	'success': True,
	'context': 'login',
	'errors' : {
		'login': '',
		...
	}
}

Improvement
-----------
- If some user is already logged in, then first log him out ant then allow the new user to login.
"""
# Do unit testing
def login(request):
	context=u'login'
	(valid, user, response) = prepare_status_for(request, context, forms.LoginForm)
	if valid:
		u = auth.authenticate(username=user['username'], password=user['password'])
		if u is not None and u.is_active:
			# Correct password, and the user is marked "active"
			auth.login(request, u)
			return HttpResponseRedirect(c.REDIRECT_SUCCESSFUL_LOGIN)
		else:
			# Authentication failed
			return HttpResponseRedirect(c.REDIRECT_UNSUCCESSFUL_LOGIN)
	return http_wrap_json(response)

"""
login() view. Special login page for redirects.
"""
# Do unit testing
def login_special(request):
	# if request.user:
	# 	return HttpResponseRedirect('/dashboard/')
	if 'next' in request.GET:
		return render_to_response('authentication-index.html', {
					'redirect': request.GET['next']
				}, RequestContext(request))
	else:
		return render_to_response('authentication-index.html', {
				'redirect': ''
			}, RequestContext(request))

"""
login_no_redirect() view. Made for use with the extension.

Input JSON keys
- username: 'mitthu'
- password: 'password'

Returns
{
	'for_username': 'mitthu',
	'redirect': '/dahboard/'
	'success': True,
	'context': 'login_no_redirect',
	'errors' : {
		'login_no_redirect': '',
		...
	}
}

Improvement
-----------
- If some user is already logged in, then first log him out ant then allow the new user to login.
"""
def login_no_redirect(request):
	context=u'login_no_redirect'
	(valid, user, response) = prepare_status_for(request, context, forms.LoginForm)
	response['redirect'] = c.REDIRECT_UNSUCCESSFUL_LOGIN
	if valid:
		u = auth.authenticate(username=user['username'], password=user['password'])
		if u is not None and u.is_active:
			# Correct password, and the user is marked "active"
			auth.login(request, u)
			response['success'] = True
			response['redirect'] = c.REDIRECT_SUCCESSFUL_LOGIN
		else:
			# Authentication failed
			response['success'] = False
			response['errors'][context] = c.ERR_CREDNTIALS
			response['redirect'] = c.REDIRECT_UNSUCCESSFUL_LOGIN
	return http_wrap_json(response)


"""
login_status() view. Made for use with the web-app.

Input JSON keys
- None

Returns
- None

Improvement
-----------
"""
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(c.REDIRECT_LOGOUT)

"""
login_status() view. Made for use with the extension.

Input JSON keys
- None

Returns
{
	'username': 'mitthu'.
	'success': True,
	'context': 'login_status',
	'errors' : {
		'login_status': '',
		...
	}
}

Improvement
-----------
"""
def logout_no_redirect(request):	
	context = u'logout_no_redirect'
	response = get_default_response_status(context)
	response['username'] = request.user.username

	auth.logout(request)
	response['success'] = True

	return http_wrap_json(response)

"""
login_status() view. Made for use with the extension.

Input JSON keys
- None

Returns
{
	'username': 'mitthu',
	'success': True,
	'context': 'login_status',
	'errors' : {
		'login_status': '',
		...
	}
}

Improvement
-----------
"""
def login_status(request):
	context = u'login_status'
	response = get_default_response_status(context)

	if request.user.is_authenticated():
		response['success'] = True
		response['username'] = request.user.username
	else:
		response['success'] = False
		response['errors'][context] = c.ERR_NOT_LOGGED_IN

	return http_wrap_json(response)
