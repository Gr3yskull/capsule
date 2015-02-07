# Started on 27-Jan-2013; 1:00 PM, by mitthu
# My Ambitious Project....

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Template, RequestContext
from notes.models import Note

def notes(request):
	return render_to_response('notes-index.html', {}, RequestContext(request))

def fetch(request):
	notes = Note.objects.all()
	data = "<tr>"
	data += "<th>" + "#" + "</th>"
	data += "<th>" + "Name" + "</th>"
	data += "<th>" + "Content" + "</th>"
	data += "</tr>"

	i = 0
	for note in notes:
		i = i+1
		data += "<tr>"
		data += "<td>" + str(i) + "</td>"
		data += "<td>" + note.name + "</td>"
		data += "<td>" + note.content + "</td>"
		data += "</tr>"

	return HttpResponse(data)

def save_data(request):
	if 'name' in request.GET and request.GET['name'] and 'content' in request.GET and request.GET['content']:
		name = request.GET['name']
		content = request.GET['content']

		note = Note(name=name, content=content)
		note.save()

		return HttpResponse('Successful')
	else:
		return HttpResponse('Failed')
