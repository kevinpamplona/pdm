from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect
from os import curdir, sep
import json
import models

# Create your views here.
class RenderView(View):
	def get(self, request, *args, **kwargs):
		assert False

	def post(self, request, *args, **kwargs):
		data_in = json.loads(request.body)
		width = data_in['width']
		height = data_in['height']
		data = data_in['data']
		owner = request.user.username if request.user.is_authenticated() else ''
		if request.path == '/stage/render':
			data_out = models.pdm_stages.render(width, height, data, owner)
			response = {"stageid" : data_out}
			j_resp = json.dumps(response)
			return HttpResponse(content=j_resp, content_type='application/json', status=200)
		else:
			assert False

class EditorView(View):
	def get(self, request, *args, **kwargs):
		f = open(curdir + sep + request.path + '.html')
		response = HttpResponse(content=f.read(), content_type='text/html', status=200)
		f.close()
		return response

	def post(self, request, *args, **kwargs):
		assert False
