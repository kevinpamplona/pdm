from os import curdir, sep
from django.http import HttpResponse

def static_page(request):
    page = 'static_pages/index' if request.path == '/' else request.path
    f = open(curdir + sep + page + '.html')
    response = HttpResponse(content=f.read(), content_type='text/html', status=200)
    f.close()
    return response
