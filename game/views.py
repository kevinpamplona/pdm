from django.shortcuts import render

from django.views.generic import View
from django.http import HttpResponse, Http404

# Create your views here.
class HandlerView(View):
    def get(self, request, *args, **kwargs):
        from django.conf import settings
        print settings.STATIC_ROOT

        from os import curdir, sep
        try:
            f = open(curdir + sep + request.path)
        except (IOError):
            raise Http404

        if request.path.endswith(".html"):
            _content_type = 'text/html'
        elif request.path.endswith(".css"):
            _content_type = 'text/css'
        elif request.path.endswith(".js"):
            _content_type = 'text/javascript'
        else:
            assert False

        send_out = HttpResponse(content=f.read(), content_type=_content_type)
        f.close()
        return send_out