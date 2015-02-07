# Started on 26-Feb-2013; 3:37 PM, by mitthu

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Template, RequestContext

from django.contrib import auth
from django.contrib.auth.models import User
import json
from Log import *
import forms

# Login Status, v1: Initially, part of the 'capsule' app, and named 'misc_login_status'. Proper response wrapping not carried out.
def login_status(request):
	login_status = {}
	login_status[u'status'] = False

	# Get username. If user is not logged in, then the username is blank (i.e. annonymous user)
	login_status[u'username'] = request.user.username

	# Checking authentication status
	if request.user.is_authenticated():
		login_status[u'status'] = True

	return HttpResponse(json.dumps(login_status), content_type="application/json")

# Login, v1: Uses regular form POST and not JSON.
def login_v1(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	if user is not None and user.is_active:
		# Correct password, and the user is marked "active"
		auth.login(request, user)
		return HttpResponseRedirect("/dashboard/")
	else:
		# Authentication failed
		return HttpResponseRedirect("/")

# SignUp, v1
"""
Input JSON keys
- username
- password
- email
- first_name
- last_name
"""
def signup_v1():
	log.info("New user signup");
	status = {}
	status['success'] = False
	status['context'] = 'signup'

	if request.is_ajax() and request.method == 'POST':
		try:
			new_user = json.loads(request.raw_post_data)
		except:
			log.error("Invalid json submitted for signup.");
			new_user = {}
			pass

		# Creating a new user
		if 	new_user['username'] is not None and new_user['password'] is not None and new_user['email'] is not None:
			
			u = User()
			u.username=new_user['username']
			u.set_password(new_user['password'])
			u.email=new_user['email']
			
			if new_user['first_name'] is not None:
				u.first_name = new_user['first_name']
			if new_user['last_name'] is not None:
				u.last_name = new_user['last_name']
		try:
			u.save()
			status['success'] = True
		except:
			log.error("Error saving new user");
			pass
	return HttpResponse(json.dumps(success), content_type="application/json")

# SignUp, v2
"""
Input JSON keys
- username
- password
- email
- first_name
- last_name
"""
def signup_v2(request):
	log.info("New user signup");
	status = {}
	status['success'] = False
	status['context'] = 'signup'
	status['errors'] = {}

	# if request.is_ajax() and request.method == 'POST':
	if request.method == 'POST':
		try:
			new_user = json.loads(request.raw_post_data)
		except:
			err = "Invalid json submitted for signup: %s" % (request.raw_post_data)
			log.error(err)
			status['errors']['signup'] = 'Invalid data posted.'
			return HttpResponse(json.dumps(status), content_type="application/json")

		# Creating a new user
		if 'username' in new_user and 'password' in new_user:
			try:
				user = User.objects.get(username=new_user['username'])
				# If user already exists
				status['errors']['signup'] = 'User already exists.'
			except User.DoesNotExist:
				u = User()
				u.username=new_user['username']
				u.set_password(new_user['password'])

				if 'email' in new_user:
					u.email=new_user['email']			
				if 'first_name' in new_user:
					u.first_name = new_user['first_name']
				if 'last_name' in new_user:
					u.last_name = new_user['last_name']
				try:
					u.save()
					status['success'] = True
				except:
					log.error("Error saving new user");
					pass
	return HttpResponse(json.dumps(status), content_type="application/json")

# SignUp, v3
"""
Input JSON keys
- username
- password
- email
- first_name
- last_name
"""
def signup_v3(request):
	status = {}
	status['success'] = False
	status['context'] = 'signup'
	status['errors'] = {}
	status['errors']['signup'] = 'Method is not Ajax.'

	if request.is_ajax() and request.method == 'POST':
		try:
			new_user = json.loads(request.raw_post_data)
			if 'username' in new_user:
				log.info("New user signup: %s" % (new_user['username']));
		except:
			log.error("Invalid json submitted for signup: %s" % (request.raw_post_data))
			status['errors']['signup'] = 'Invalid data posted.'
			return HttpResponse(json.dumps(status), content_type="application/json")

		form = forms.SignupForm(new_user)
		if form.is_valid():
			new_user = form.cleaned_data
			try:
				user = User.objects.get(username=new_user['username'])
				# If user already exists
				status['errors']['signup'] = 'User already exists.'
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
					status['success'] = True
				except:
					log.error("Error saving new user");
					status['errors']['signup'] = 'Error saving new user.'
					pass
		else:
			# Updating error list
			status['errors']['signup'] = 'Failed due to invalid form entries.'
			status['errors'] = dict(status['errors'].items() + form.errors.items())
	
	return HttpResponse(json.dumps(status), content_type="application/json")

# SignUp, v4: Implemented auto form updates
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
def signup_v4(request):
	(valid, new_user, response) = prepare_status_for(request, 'signup')
	if valid:
		form = forms.SignupForm(new_user)
		if form.is_valid():
			new_user = form.cleaned_data
			try:
				user = User.objects.get(username=new_user['username'])
				# If user already exists
				response['errors']['signup'] = 'User already exists.'
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
					log.error("Error saving new user");
					response['errors']['signup'] = 'Error saving new user.'
					pass
		else:
			# Updating error list
			response['errors']['signup'] = 'Failed due to invalid form entries.'
			response['errors'] = dict(response['errors'].items() + form.errors.items())
	return http_wrap_json(response)
