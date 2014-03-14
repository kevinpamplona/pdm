from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
import json
import subprocess
from subprocess import CalledProcessError
import re
import models


class HandlerView(View):
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
		data_in = json.loads(request.body)
		username = data_in['user']
		password = data_in['password']

		if request.path == '/users/login':
			data_out = models.g_users.login(username, password)
			#return HttpResponse(str(data_out) + ' -- Hello, POST-LOGIN request!\n')
		else:
			data_out = models.g_users.add(username, password)
			#return HttpResponse(str(data_out) + ' -- Hello, POST-ADD request!\n')
		if data_out < 0:
			response = {"errCode" : data_out}
		else:
			response = {"errCode" : models.g_users.SUCCESS, "count" : data_out}

		j_resp = json.dumps(response)
		print "data out: " + j_resp

		return HttpResponse(content=j_resp, content_type='application/json', status=200)



class ResetView(View):
	def post(self, request, *args, **kwargs):
		models.g_users.TESTAPI_resetFixture()
		response = {"errCode" : models.g_users.SUCCESS}
		data_out = json.dumps(response)
		return HttpResponse(content=data_out, content_type='application/json', status=200)

class TestView(View):
	def post(self, request, *args, **kwargs):
		try:
			test_results = subprocess.check_output(['python', 'manage.py', 'test', 'users.tests'], stderr=subprocess.STDOUT)
			regex = re.compile('[EF.]{2,}')
			match = regex.match(test_results).group()
			totalTests = len(match)
			response = {"nrFailed" : 0, "output" : test_results, "totalTests" : totalTests }
			data_out = json.dumps(response)
			return HttpResponse(content=data_out, content_type='application/json', status=200)
		except CalledProcessError as error_result:
			response = {"nrFailed" : 0, "output" : error_result, "totalTests" : 25}
			test_data = json.dumps(response)
			return HttpResponse(content=test_data, content_type='application/json', status=200) # comment out before submission
			regex = re.compile('[EF.]{2,}')
			print "***************#@#@******************" + error_result.output 
			match = regex.match(error_result.output).group()
			totalTests = len(match)
			failures = 0
			for ch in match:
				if ch != '.':
					failures = failures + 1
			response = {"nrFailed" : failures, "output" : error_result.output, "totalTests" : totalTests }
			data_out = json.dumps(response)
			return HttpResponse(content=data_out, content_type='application/json', status=200)