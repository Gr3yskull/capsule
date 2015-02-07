"""
Started on 26-Mar-2013; 5:00 PM, by mitthu
Part of the -( capsule )- project
"""

from django import forms

class SignupForm(forms.Form):
	username = forms.CharField(max_length=30, required=True, help_text="Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters")
	password = forms.CharField(max_length=30, required=True)
	email = forms.EmailField(required=True)
	first_name = forms.CharField(max_length=30, required=False)
	last_name = forms.CharField(max_length=30, required=False)

class ResetPasswordForm(forms.Form):
	username = forms.CharField(max_length=30, required=True, help_text="Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters")
	email = forms.EmailField(required=True)

class LoginForm(forms.Form):
	username = forms.CharField(max_length=30, required=True, help_text="Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters")
	password = forms.CharField(max_length=30, required=True)

class UserAvailabilityForm(forms.Form):
	username = forms.CharField(max_length=30, required=True, help_text="Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters")

class DeleteAccountForm(forms.Form):
	username = forms.CharField(max_length=30, required=True, help_text="Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters")
	password = forms.CharField(max_length=30, required=True)

class ModifyUserForm(forms.Form):
	username = forms.CharField(max_length=30, required=True, help_text="Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters")
	password = forms.CharField(max_length=30, required=True)
	new_username = forms.CharField(max_length=30, initial=None, required=False, help_text="Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters")
	new_password = forms.CharField(max_length=30, initial=None, required=False)
	new_email = forms.EmailField(required=False, initial=None)
	new_first_name = forms.CharField(max_length=30, initial=None, required=False)
	new_last_name = forms.CharField(max_length=30, initial=None, required=False)
