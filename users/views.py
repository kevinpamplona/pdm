from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
import json
import subprocess
from subprocess import CalledProcessError
import re
#import models
from users.models import UserForm, UsersModel
from stage.models import Stage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

errors = {
    UsersModel.ERR_BAD_CREDENTIALS: "The username and/or password you entered is incorrect.",
    UsersModel.ERR_USER_EXISTS:  "The username already exists",
    UsersModel.ERR_BAD_PASSWORD: "Your password exceeds 256 characters.",
    None: "Please enter your credentials below", # This one should never appear
}

# Create your views here.
def get_login(request):
    context = {'message' : ""}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if u'logout' in form.data:
            logout(request)
            return redirect('/')
        username = form.data[u'username']
        password = form.data[u'passwd']
        if u'login' in form.data:
            user = authenticate(username = username, password = password)
            if user is not None and user.is_active:
                login(request, user)
                result = UsersModel.SUCCESS
            else:
                result = UsersModel.ERR_BAD_CREDENTIALS
        elif u'adduser' in form.data:
            if User.objects.filter(username = username):
                result = UsersModel.ERR_USER_EXISTS
            elif len(username) == 0 or len(username) > UsersModel.MAX_USERNAME_LENGTH:
                result = UsersModel.ERR_BAD_USERNAME
            elif len(password) > UsersModel.MAX_PASSWORD_LENGTH:
                result = UsersModel.ERR_BAD_PASSWORD
            else:
                new_user = User.objects.create_user(username, '', password)
                new_user.save()
                new_user = authenticate(username = username, password = password)
                login(request, new_user)
                result = UsersModel.SUCCESS
        else:
            result = None # This should never be reached

        if result == UsersModel.SUCCESS:
            return redirect('/game')
        elif result == UsersModel.ERR_BAD_USERNAME:
            context['message'] = "ADD USER ERROR: Username is " + ("empty" if len(username) == 0 else "too long")
        else:
            context['message'] = errors[result]
    elif request.user.is_authenticated():
        return redirect('/')
    else:
        form = UserForm()

    context['form'] = form
    return render(request, 'static_pages/index.html', context)


def search(request):
    if request.method == 'GET':
        form = UserForm(request.GET)
        query = form.data[u'query']

        context = {}
        context = {'query' : query}

        if User.objects.filter(username=query):
            context['user_exists'] = "true"
            context['username'] = query
            context['user_stagecount'] = Stage.objects.filter(owner=query).count() 

            context['user_stages'] = []
            for stage in Stage.objects.filter(owner=query):
                context['user_stages'].append(stage)
            #context['user_result'] = "USER EXISTS"
        else:
            context['user_exists'] = "false"
            #context['user_result'] = "USER DOES NOT EXIST"

        if Stage.objects.filter(name=query):
            context['stages_exists'] = "true"
            context['stages_stagecount'] = Stage.objects.filter(name=query).count()

            context['stages_stages'] = []
            for stage in Stage.objects.filter(name=query):
                 context['stages_stages'].append(stage)

        else:
            context['stages_exists'] = "false"

        return render(request, 'users/search.html', context)
    else:
        context = {}
        return render(request, 'users/search.html', context)
        # should not be reached

def profile(request):
    if request.method == 'GET':
        form = UserForm(request.GET)
        user = form.data[u'user']

        context = {'user' : user, 'logged_in': True}

        if User.objects.filter(username=user):
            context['user_exists'] = "true"
            context['username'] = user
            context['user_stagecount'] = Stage.objects.filter(owner=user).count() 

            context['user_stages'] = []
            for stage in Stage.objects.filter(owner=user):
                context['user_stages'].append(stage)
            #context['user_result'] = "USER EXISTS"
        else:
            context['user_exists'] = "false"
            #context['user_result'] = "USER DOES NOT EXIST"

        return render(request, 'users/profile.html', context)
    else:
        context = {}
        return render(request, 'users/profile.html', context)
        # should not be reached

def browse(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'users/browse.html', context)
    else:
        context = {}
        return render(request, 'users/browse.html', context)
        # should not be reached

class HandlerView(View): # Deprecated view
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
