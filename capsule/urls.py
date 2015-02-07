# Started on 31-Mar-2013; 10:25 AM, by mitthu
# The -( capsule )- project

from django.conf.urls.defaults import patterns
from capsule.views import *

urlpatterns = patterns('',
# User Api
	(r'^$'                             , homepage),
	(r'^page/(?P<page_number>\d*)/?$'  , page),
	(r'^search/(?P<page_number>\d*)/?$', search),
	# (r'^filter/(?P<page_number>\d*)/?$', page),
	(r'^add/$'                         , add),
	(r'^delete/$'                      , delete),
	(r'^modify/$'                      , modify),
	(r'^tags_frequency/$'              , tags_frequency),
	# Deprecated
	# (r'^page_html/(?P<page_number>\d*)/?$', page_html),
	# (r'^misc/colour_codes/$'              , misc_colour_codes),
)
