# Started on 24-Feb-2013; 7:30 PM, by mitthu
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Template, RequestContext
from django.contrib.auth.decorators import login_required

from library.log import log
# from json import JSONEncoder, JSONDecoder
import json as j

@login_required
def home(request):
	log.info("Dashboard home requested");
	return render_to_response('dashboard-index.html', {
					'base_url': 'https://home.adityabasu.me/',
					'portal_attr': 'tabindex="-1"  target="_blank"' # For <a> tag
				}, RequestContext(request))

@login_required
def json(request):
	log.info("Dashboard json requested");
	if request.is_ajax():
		if request.method == 'POST':
			log.info('Posted Raw Data: "%s"' % request.raw_post_data)
	json_data = {
				"name": "mitthu"
			}
	# return HttpResponse(JSONEncoder().encode(json))
	return HttpResponse(j.dumps(json_data), content_type="application/json")

@login_required
def get_highlights(request):
	log.info("Highlights requested")
	json_data = {"highlights": [
					'Maff',
					'Uploads',
					'Notes'
				]}
	return HttpResponse(j.dumps(json_data), content_type="application/json")
	