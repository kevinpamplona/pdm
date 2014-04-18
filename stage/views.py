from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect
from django.core.exceptions import ObjectDoesNotExist
from os import curdir, sep
from stage.models import Stage
import json
import models

# Create your views here.

class RenderView(View):
	def get(self, request, *args, **kwargs):
		assert False

	def post(self, request, *args, **kwargs):
		data_in = json.loads(request.body)
		width = int(data_in['width'])
		height = int(data_in['height'])
		name = data_in['name']
		data = data_in['data']
		stageid = data_in['id']
		owner = request.user.username if request.user.is_authenticated() else ''
		if request.path == '/stage/render':
			if stageid is None:
				stageid = models.pdm_stages.render(width, height, name, data, owner)
			else:
				try:
					stage = Stage.objects.get(pk=stageid)
					stage.data = data
					stage.width = width
					stage.height = height
					stage.save()
				except ObjectDoesNotExist:
					stageid = models.pdm_stages.render(width, height, name, data, owner)
				except Exception as e:
					print e
					raise
			response = {"stageid" : stageid}
			j_resp = json.dumps(response)
			return HttpResponse(content=j_resp, content_type='application/json', status=200)
		else:
			assert False

class EditorView(View):
	def get(self, request, *args, **kwargs):
		context = {}
		if u'stageid' in request.GET:
			try:
				stage = Stage.objects.get(pk=request.GET[u'stageid'])
				if (request.user.is_authenticated() and request.user.username == stage.owner) or  stage.owner == '':
					response_data = {}
					response_data['width'] = stage.width
					response_data['height'] = stage.height
					response_data['data'] = stage.data.replace('\n', '\\n').replace('\r', '')
					response_data['stageid'] = stage.pk
					context['data'] = json.dumps(response_data)
					#print(stage.data)
				else:
					context['error'] = "You can't edit another user's stage! Creating new stage"
			except ObjectDoesNotExist:
				context['error'] = "Cannot edit nonexistant stage! Creating new stage"
			except Exception as e:
				print e
				raise
		return render(request, 'stage/editor.html', context)

	def post(self, request, *args, **kwargs):
		assert False

class VoteView(View):
	def get(self, request, *args, **kwargs):
		assert False

	def post(self, request, *args, **kwargs):
		data_in = json.loads(request.body)

		vote = data_in['vote']
		stageid = int(data_in['stageid'])

		if vote == 'up':
			# upvote
			new_rating = models.pdm_stages.upvote(stageid)
		else:
			# downvote
			new_rating = models.pdm_stages.downvote(stageid)

		response = {'new_rating' : new_rating}
		j_resp = json.dumps(response)
		return HttpResponse(content=j_resp, content_type='application/json', status=200)
