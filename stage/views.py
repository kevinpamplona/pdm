from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect
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
		owner = data_in['owner']
		if request.path == '/stage/render':
			data_out = models.pdm_stages.render(width, height, data, owner)
			response = {"stageid" : data_out}
			j_resp = json.dumps(response)
			print "test test test test"
			return HttpResponse(content=j_resp, content_type='application/json', status=200)
		else:
			assert False

class EditorView(View):
	def get(self, request, *args, **kwargs):

		from os import curdir, sep
		f = open(curdir + sep + request.path)

		if request.path.endswith(".html"):
			_content_type = 'text/html'
		elif request.path.endswith(".css"):
			_content_type = 'text/css'
		elif request.path.endswith(".js"):
			_content_type = 'text/javascript'
		else:
			assert False

		send_out = HttpResponse(content=f.read(), content_type=_content_type, status=200)
		f.close()
		return send_out

	def post(self, request, *args, **kwargs):
		assert False