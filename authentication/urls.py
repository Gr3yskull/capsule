# Started on 30-Mar-2013; at night, by mitthu
# The -( capsule )- project

from django.conf.urls.defaults import patterns
from authentication.views import *

urlpatterns = patterns('',
# User Api
	(r'^signup/$'            , signup),
	(r'^login/$'             , login),
	(r'^reset_password/$'    , reset_password),
	(r'^login_no_redirect/$' , login_no_redirect),
	(r'^logout/$'            , logout),
	(r'^login_status/$'      , login_status),
	(r'^logout_no_redirect/$', logout_no_redirect),
	(r'^modify/$'            , modify),
	(r'^username_available/$', username_available),
	(r'^delete_account/$'    , delete_account),
)
