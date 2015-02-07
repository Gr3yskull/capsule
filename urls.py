from django.conf.urls.defaults import patterns, include, url

from django.contrib.auth.views import login, logout

import dashboard.views as dash
import authentication.views as a
import capsule.views as c

import authentication.urls
import capsule.urls

# Exception Handlers
handler404 = 'dashboard.views.home'

urlpatterns = patterns('',
# TODO
# - Handle the 'next' parameter to login.
# Authentication
	(r'^$', c.homepage),
	(r'^auth/$', a.home),
	(r'^dashboard/$', dash.home),
	(r'^login/$', a.login),
	(r'^logout/$', a.logout),
	# @login_required redirects here
	(r'^accounts/login/$',  a.login_special),
    (r'^accounts/logout/$', a.logout),

# Api
	# User API
	(r'^api/user/', include(authentication.urls)),
	(r'^api/notes/', include(capsule.urls)),
	# Deprecated
	# (r'^api/misc/login_status/$', capsule.misc_login_status),
)
