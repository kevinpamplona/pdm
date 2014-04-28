from os import curdir, sep
from django.http import HttpResponse
from django.shortcuts import render


# def static_page(request):
#     page = 'static_pages/index' if request.path == '/' else request.path
#     f = open(curdir + sep + page + '.html')
#     response = HttpResponse(content=f.read(), content_type='text/html', status=200)
#     f.close()
#     return response

def static_asset(request):
    f = open(curdir + sep + request.path)
    if request.path.endswith(".html"):
            _content_type = 'text/html'
    elif request.path.endswith(".css"):
            _content_type = 'text/css'
    elif request.path.endswith(".js"):
            _content_type = 'text/javascript'
    else:
            assert False
    response = HttpResponse(content=f.read(), content_type=_content_type, status=200)
    f.close()
    return response

def static_page(request):
    context = {}
    context['message'] = "Whats up, dawg?"
    if request.method == 'GET':
        if request.user.is_authenticated():
            context['logged_in'] = True
        else:
            context['logged_in'] = False
    else:
        # should not reach here
        context['message'] = "Yo, you wrong!"

    render(request, 'static_pages/index.html', context)

        
