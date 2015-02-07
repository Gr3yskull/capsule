
"""
Started on 29-Mar-2013; 5:00 PM, by mitthu
The -( capsule )- project.

These tests will pass when you run "manage.py test".
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib import auth
from django.contrib.auth.models import User, check_password
import json
import forms, views, constants as c
from library.log import log

"""Assumption: Signup Feature is working properly."""
def create_user(user, password, email=None, first_name=None, last_name=None):
	new_user = {'username': user, 'password': password, 'email': email, 'first_name': first_name, 'last_name': last_name}
	Client().post('/api/user/signup/', data=json.dumps(new_user), content_type='application/json', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

"""
This tests the login system.
Affected views:
- login() @ /api/user/login
- login_no_redirect() @ /api/user/login_no_redirect
- login_status() @ /api/user/login_status
- logout() @ /api/user/logout
- logout_no_redirect() @ /api/user/logout_no_redirect

Template
--------
self.input[''] = ''

Improvement
-----------
- Check for invalid JSON posting.
"""
class LoginSystemTest(TestCase):
	def setUp(self):
		self.client = Client()
		self.input = {}
		create_user('aditya', 'password_1')
		create_user('mitthu', 'password_2')

	def get_response(self, view):
		self.response = self.client.post('/api/user/%s/' % view, data=json.dumps(self.input), content_type='application/json', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		# Decoding json would fail for redirects.
		try:
			self.content = json.loads(self.response.content)
			self.success = self.content['success']
			self.errors = self.content['errors']
			self.error_context = self.errors[view]
		except:
			pass
		
	def test_invalid_username_login_no_redirect(self):
		self.input['username'] = 'adityaMitthu'
		self.input['password'] = 'password_1'
		self.get_response('login_no_redirect')
		self.assertEqual(self.success, False)
		self.assertEqual(self.content['redirect'], c.REDIRECT_UNSUCCESSFUL_LOGIN)

	def test_invalid_password_login_no_redirect_v1(self):
		self.input['username'] = 'aditya'
		self.input['password'] = 'password'
		self.get_response('login_no_redirect')
		self.assertEqual(self.success, False)
		self.assertEqual(self.content['redirect'], c.REDIRECT_UNSUCCESSFUL_LOGIN)

	def test_invalid_password_login_no_redirect_v2(self):
		self.input['username'] = 'aditya'
		self.input['password'] = ''
		self.get_response('login_no_redirect')
		self.assertEqual(self.success, False)
		self.assertEqual(self.content['redirect'], c.REDIRECT_UNSUCCESSFUL_LOGIN)

	def test_invalid_combination_login(self):
		self.input['username'] = 'adityaMitthu'
		self.input['password'] = 'password_1'
		self.get_response('login')
		self.assertEqual(self.response.redirect_chain[0][0], u'http://testserver'+c.REDIRECT_UNSUCCESSFUL_LOGIN)

	def test_invalid_login_status(self):
		self.get_response('login_status')
		self.assertEqual(self.success, False)
		self.assertEqual(self.error_context, c.ERR_NOT_LOGGED_IN)

	# Logging out when no user is logged in
	def test_invalid_logout(self):
		self.get_response('logout')
		self.assertEqual(self.response.redirect_chain[0][0], u'http://testserver'+c.REDIRECT_LOGOUT)

	def test_valid_combination_login(self):
		self.input['username'] = 'mitthu'
		self.input['password'] = 'password_2'
		self.get_response('login')
		self.assertEqual(self.response.redirect_chain[0][0], u'http://testserver'+c.REDIRECT_SUCCESSFUL_LOGIN)

	def test_valid_combination_login_no_redirect(self):
		self.input['username'] = 'mitthu'
		self.input['password'] = 'password_2'
		self.get_response('login_no_redirect')
		self.assertEqual(self.success, True)
		self.assertEqual(self.content['redirect'], c.REDIRECT_SUCCESSFUL_LOGIN)

	def test_valid_comprehensive_no_redirects(self):
		# Login as 'mitthu'
		self.input['username'] = 'mitthu'
		self.input['password'] = 'password_2'
		self.get_response('login_no_redirect')
		self.assertEqual(self.success, True)
		self.assertEqual(self.content['redirect'], c.REDIRECT_SUCCESSFUL_LOGIN)

		# Verifying login status
		self.get_response('login_status')
		self.assertEqual(self.success, True)
		self.assertEqual(self.content['username'], 'mitthu')

		# Logging out
		self.get_response('logout_no_redirect')
		self.assertEqual(self.success, True)
		self.assertEqual(self.content['username'], 'mitthu')

		# Reverifying login status after logout
		# Note: There is no self.content['username'], as no user is logged in.
		self.get_response('login_status')
		self.assertEqual(self.success, False)
		# log.info('test_valid_comprehensive_no_redirects: %s' % self.content)
		self.assertEqual(self.error_context, c.ERR_NOT_LOGGED_IN)

"""
This tests the modify view @ /api/user/modify.

Template
--------
self.input[''] = ''

Improvement
-----------
"""
class ModifyUserAccountTest(TestCase):
	def setUp(self):
		self.client = Client()
		self.input = {}

	def get_response(self):
		self.response = self.client.post('/api/user/modify/', data=json.dumps(self.input), content_type='application/json', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.content = json.loads(self.response.content)
		self.success = self.content['success']
		self.errors = self.content['errors']
		self.error_context = self.errors['modify']

	def test_invalid_json(self):
		self.input = 'invalid_json'
		self.response = self.client.post('/api/user/modify/', data=self.input, content_type='application/json', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.content = json.loads(self.response.content)
		self.success = self.content['success']
		self.errors = self.content['errors']
		self.error_context = self.errors['modify']

		self.assertEqual(self.success, False)
		self.assertEqual(self.error_context, 'Posted data format is invalid.')

	def test_invalid_username(self):
		self.input['username'] = ''
		self.get_response()
		self.assertEqual(self.success, False)
		self.assertEqual(self.error_context, 'Failed due to invalid form entries.')

	def test_invalid_password(self):
		self.input['username'] = 'aditya'
		self.input['password'] = ''
		self.get_response()
		self.assertEqual(self.success, False)
		
	def test_invalid_email(self):
		self.input['username'] = 'AdityaBasu'
		self.input['password'] = 'abascus'
		self.input['new_email'] = 'abc@gmail'
		self.get_response()
		self.assertEqual(self.success, False)

	# Correct test
	# Failed:
	# AssertionError: u'Nothing was changed.' != 'Please check your credentials.'
	def test_invalid_user_does_not_exist(self):
		create_user('aditya', 'password')
		self.input['username'] = 'mitthu'
		self.input['password'] = 'password'
		self.get_response()
		self.assertEqual(self.success, False)
		# log.info("test_invalid_user_does_not_exist: %s" % self.errors)
		# self.assertEqual(self.error_context, 'User does not exist.')
		self.assertEqual(self.error_context, 'Please check your credentials.')

	# Correct test
	# Failed:
	# AssertionError: u'Nothing was changed.' != 'Please check your credentials.'
	def test_invalid_user_not_authorized(self):
		create_user('aditya', 'password')
		self.input['username'] = 'aditya'
		self.input['password'] = 'password_2'
		self.get_response()
		self.assertEqual(self.success, False)
		# log.info("test_invalid_user_not_authorized: %s" % self.errors)
		self.assertEqual(self.error_context, 'Please check your credentials.')

	# Username already exists
	def test_invalid_username_modified(self):
		create_user('aditya', 'password')
		create_user('mitthu', 'password')
		new_username = 'mitthu'

		self.input['username'] = 'aditya'
		self.input['password'] = 'password'
		self.input['new_username'] = new_username
		self.get_response()
		
		self.assertEqual(self.success, False)
		self.assertEqual(self.error_context, 'Username already exists.')

	def test_invalid_email_modified(self):
		create_user('aditya', 'password', email="")
		new_username = 'mitthu'
		new_email = 'xyz@.com'

		self.input['username'] = 'aditya'
		self.input['password'] = 'password'
		self.input['new_username'] = new_username
		self.input['new_email'] = new_email
		self.get_response()
		
		self.assertEqual(self.success, False)
		# Checked against the old values because of atomic nature of the modify() view.
		self.assertNotEqual(User.objects.get(username='aditya').email, new_email)

	def test_valid_username_modified(self):
		create_user('aditya', 'password')
		new_username = 'mitthu'

		self.input['username'] = 'aditya'
		self.input['password'] = 'password'
		self.input['new_username'] = new_username
		self.get_response()
		
		self.assertEqual(self.success, True)
		self.assertIsNotNone(User.objects.get(username=new_username))

	def test_valid_password_modified(self):
		create_user('aditya', 'password')
		new_password = 'password_2'

		self.input['username'] = 'aditya'
		self.input['password'] = 'password'
		self.input['new_password'] = new_password
		self.get_response()
		
		self.assertEqual(self.success, True)
		self.assertTrue(User.objects.get(username=self.input['username']).check_password(new_password))

	def test_valid_username_and_password_modified(self):
		create_user('aditya', 'password')
		new_username = 'mitthu'
		new_password = 'password_2'

		self.input['username'] = 'aditya'
		self.input['password'] = 'password'
		self.input['new_username'] = new_username
		self.input['new_password'] = new_password
		self.get_response()
		
		self.assertEqual(self.success, True)
		self.assertTrue(User.objects.get(username=new_username).check_password(new_password))
		# Alternative
		# -----------
		# self.assertIsNotNone(auth.authenticate(username=new_username, password=new_password))

	def test_valid_email_modified_v1(self):
		create_user('aditya', 'password', email="abc@gmail.com")
		new_username = 'mitthu'
		new_email = 'xyz@gmail.com'

		self.input['username'] = 'aditya'
		self.input['password'] = 'password'
		self.input['new_username'] = new_username
		self.input['new_email'] = new_email
		self.get_response()
		
		self.assertEqual(self.success, True)
		self.assertEqual(User.objects.get(username=new_username).email, new_email)

	def test_valid_email_modified_v2(self):
		create_user('aditya', 'password', email="")
		new_username = 'mitthu'
		new_email = 'xyz@gmail.com'

		self.input['username'] = 'aditya'
		self.input['password'] = 'password'
		self.input['new_username'] = new_username
		self.input['new_email'] = new_email
		self.get_response()
		
		self.assertEqual(self.success, True)
		self.assertEqual(User.objects.get(username=new_username).email, new_email)

	def test_valid_overall(self):
		old_last_name = 'basu'
		create_user('aditya', 'password', 'abc@gamil.com', 'Aditya', old_last_name)
		new_username = 'mitthu'
		new_email = 'xyz@gmail.com'
		new_last_name = 'Basu'

		self.input['username'] = 'aditya'
		self.input['password'] = 'password'
		self.input['new_username'] = new_username
		self.input['new_email'] = new_email
		self.input['new_last_name'] = new_last_name
		self.get_response()
		
		self.assertEqual(self.success, True)
		self.assertEqual(User.objects.get(username=new_username).email, new_email)
		self.assertEqual(User.objects.get(username=new_username).last_name, new_last_name)
		self.assertNotEqual(User.objects.get(username=new_username).last_name, old_last_name)

"""
This tests the delete_account view @ /api/user/delete_account.

Template
--------
self.input[''] = ''

Improvement
-----------
"""
class DeleteAccountTest(TestCase):
	def setUp(self):
		self.client = Client()
		self.input = {}

	def get_response(self):
		self.response = self.client.post('/api/user/delete_account/', data=json.dumps(self.input), content_type='application/json', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.content = json.loads(self.response.content)
		self.success = self.content['success']
		self.errors = self.content['errors']
		self.error_context = self.errors['delete_account']

	def test_invalid_json(self):
		self.input = 'invalid_json'
		self.response = self.client.post('/api/user/delete_account/', data=self.input, content_type='application/json', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.content = json.loads(self.response.content)
		self.success = self.content['success']
		self.errors = self.content['errors']
		self.error_context = self.errors['delete_account']

		self.assertEqual(self.success, False)
		self.assertEqual(self.error_context, 'Posted data format is invalid.')

	def test_invalid_username(self):
		self.input['username'] = ''
		self.get_response()
		self.assertEqual(self.success, False)
		self.assertEqual(self.error_context, 'Failed due to invalid form entries.')

	def test_invalid_password_v1(self):
		self.input['username'] = 'aditya'
		self.get_response()
		self.assertEqual(self.success, False)

	def test_invalid_password_v2(self):
		self.input['username'] = 'aditya'
		self.input['password'] = ''
		self.get_response()
		self.assertEqual(self.success, False)

	def test_invalid_user_does_not_exist(self):
		create_user('aditya', 'password')
		self.input['username'] = 'mitthu'
		self.input['password'] = 'password'
		self.get_response()
		self.assertEqual(self.success, False)
		# log.info("test_invalid_user_does_not_exist: %s" % self.errors)
		# self.assertEqual(self.error_context, 'User does not exist.')
		self.assertEqual(self.error_context, 'Please check your credentials.')

	def test_invalid_user_not_authorized(self):
		create_user('aditya', 'password')
		self.input['username'] = 'aditya'
		self.input['password'] = 'password_2'
		self.get_response()
		self.assertEqual(self.success, False)
		# log.info("test_invalid_user_not_authorized: %s" % self.errors)
		self.assertEqual(self.error_context, 'Please check your credentials.')

	def test_valid_user_deleted(self):
		create_user('aditya', 'password')
		self.input['username'] = 'aditya'
		self.input['password'] = 'password'
		self.get_response()
		self.assertEqual(self.success, True)

"""
This tests the username_available view @ /api/user/username_available.

Template
--------
self.input[''] = ''

Improvement
-----------
"""
class UsernameAvailableTest(TestCase):
	def setUp(self):
		self.client = Client()
		self.input = {}

	def get_response(self):
		self.response = self.client.post('/api/user/username_available/', data=json.dumps(self.input), content_type='application/json', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.content = json.loads(self.response.content)
		self.success = self.content['success']
		self.errors = self.content['errors']
		self.error_context = self.errors['username_available']

	def test_invalid_json(self):
		self.input = 'invalid_json'
		self.response = self.client.post('/api/user/username_available/', data=self.input, content_type='application/json', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.content = json.loads(self.response.content)
		self.success = self.content['success']
		self.errors = self.content['errors']
		self.error_context = self.errors['username_available']

		self.assertEqual(self.success, False)
		self.assertEqual(self.error_context, 'Posted data format is invalid.')

	def test_invalid_username(self):
		self.input['username'] = ''
		self.get_response()
		self.assertEqual(self.success, False)
		self.assertEqual(self.error_context, 'Failed due to invalid form entries.')

	def test_invalid_already_exists(self):
		create_user('aditya', 'password')

		self.input['username'] = u'aditya'
		self.get_response()
		self.assertEqual(self.success, False)
		# log.info("test_invalid_already_exists: %s" % self.errors)
		self.assertEqual(self.error_context, 'User already exists.')

	def test_valid_compact(self):
		self.input['username'] = 'aditya'
		self.get_response()
		# log.info("test_valid_compact: %s" % self.errors)
		self.assertEqual(self.success, True)

"""
This tests the signup view @ /api/user/signup.

Template
--------
self.input[''] = ''

Improvement
-----------
- Check for comprehensive data entries.
"""
class SignupViewTest(TestCase):
	def setUp(self):
		self.client = Client()
		self.input = {}

	def get_response(self):
		self.response = self.client.post('/api/user/signup/', data=json.dumps(self.input), content_type='application/json', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.content = json.loads(self.response.content)
		self.success = self.content['success']
		self.errors = self.content['errors']
		self.error_context = self.errors['signup']

	def test_invalid_json(self):
		self.input = 'invalid_json'
		self.response = self.client.post('/api/user/signup/', data=self.input, content_type='application/json', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.content = json.loads(self.response.content)
		self.success = self.content['success']
		self.errors = self.content['errors']
		self.error_context = self.errors['signup']

		self.assertEqual(self.success, False)
		self.assertEqual(self.error_context, 'Posted data format is invalid.')

	def test_invalid_username(self):
		self.input['username'] = ''
		self.input['password'] = 'pass'
		self.get_response()
		self.assertEqual(self.success, False)
		self.assertEqual(self.error_context, 'Failed due to invalid form entries.')

	def test_invalid_password(self):
		self.input['username'] = 'aditya'
		self.input['password'] = ''
		self.get_response()
		self.assertEqual(self.success, False)
		
	def test_invalid_email(self):
		self.input['username'] = 'AdityaBasu'
		self.input['password'] = 'abascus'
		self.input['email'] = 'abc@gmail'
		self.get_response()
		self.assertEqual(self.success, False)

	def test_invalid_already_exists(self):
		self.input['username'] = 'aditya'
		self.input['password'] = 'password'
		self.get_response()
		self.assertEqual(self.success, True)
		self.input['username'] = 'aditya'
		self.input['password'] = 'password'
		self.get_response()
		self.assertEqual(self.success, False)

	def test_valid_compact(self):
		self.input['username'] = 'aditya'
		self.input['password'] = 'password'
		self.get_response()
		self.assertEqual(self.success, True)
		# The following raises exception, is user is not present in the database.
		User.objects.get(username='aditya')

"""
Thsi tests the Signup form.

Template
--------
self.input[''] = ''

Improvement
-----------
- For multiple errors, check if all errors are caught.
- For all errors, check if the correct error is caught.
"""
class SignupFromTest(TestCase):
	def setUp(self):
		self.input = {}

	def bind_data(self):
		self.form = forms.SignupForm(self.input)

	def test_incomplete(self):
		self.bind_data()
		self.assertEqual(self.form.is_valid(), False)

	def test_incomplete_username_v1(self):
		self.input['password'] = 'pass'
		self.bind_data()
		self.assertEqual(self.form.is_valid(), False)

	def test_incomplete_username_v2(self):
		self.input['username'] = ''
		self.input['password'] = 'pass'
		self.bind_data()
		self.assertEqual(self.form.is_valid(), False)

	def test_incomplete_password_v1(self):
		self.input['username'] = 'user'
		self.bind_data()
		self.assertEqual(self.form.is_valid(), False)

	def test_incomplete_password_v2(self):
		self.input['username'] = 'user'
		self.input['password'] = ''
		self.bind_data()
		self.assertEqual(self.form.is_valid(), False)

	def test_invalid_username(self):
		self.input['username'] = 'adityabasuadityabasuadityabasuadityabasu'
		self.bind_data()
		self.assertEqual(self.form.is_valid(), False)

	def test_invalid_email_v1(self):
		self.input['username'] = 'AdityaBasu'
		self.input['password'] = 'abascus'
		self.input['email'] = 'abc@gmail'
		self.bind_data()
		self.assertEqual(self.form.is_valid(), False)

	def test_invalid_email_v2(self):
		self.input['username'] = 'AdityaBasu'
		self.input['password'] = 'abascus'
		self.input['email'] = 'abc@gmail.'
		self.bind_data()
		self.assertEqual(self.form.is_valid(), False)

	def test_invalid_email_v3(self):
		self.input['username'] = 'AdityaBasu'
		self.input['password'] = 'abascus'
		self.input['email'] = 'abc@.com'
		self.bind_data()
		self.assertEqual(self.form.is_valid(), False)

	def test_invalid_multiple(self):
		self.input['username'] = 'AdityaBasu'
		self.input['password'] = 'abascus'
		self.input['email'] = 'abc@gmail.com'
		self.input['first_name'] = 'adityabasuadityabasuadityabasuadityabasu'
		self.input['last_name'] = 'adityabasuadityabasuadityabasuadityabasu'
		self.bind_data()
		self.assertEqual(self.form.is_valid(), False)

	"""Only username and password"""
	def test_valid_compact(self):
		self.input['username'] = 'AdityaBasu'
		self.input['password'] = 'abascus'
		self.bind_data()
		self.assertEqual(self.form.is_valid(), True)

	def test_valid_email_v1(self):
		self.input['username'] = 'AdityaBasu'
		self.input['password'] = 'abascus'
		self.input['email'] = ''
		self.bind_data()
		self.assertEqual(self.form.is_valid(), True)

	def test_valid_email_v2(self):
		self.input['username'] = 'AdityaBasu'
		self.input['password'] = 'abascus'
		self.input['email'] = None
		self.bind_data()
		self.assertEqual(self.form.is_valid(), True)

	def test_valid_comprehensive(self):
		self.input['username'] = 'jammer'
		self.input['password'] = 'jamming'
		self.input['email'] = 'abc@gmail.com'
		self.input['first_name'] = 'Aditya'
		self.input['last_name'] = 'Basu'
		self.bind_data()
		self.assertEqual(self.form.is_valid(), True)

