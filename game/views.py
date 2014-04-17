from django.shortcuts import render

from django.views.generic import View
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist

from stage.models import Stage, Block

import json

# Create your views here.
class HandlerView(View):
    def get(self, request, *args, **kwargs):
        from django.conf import settings

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

def load_stage(request, stage_id = 0):
    stage = None
    try:
        stage = Stage.objects.get(pk=stage_id)
    except ObjectDoesNotExist:
        stage = Stage.objects.default_stage()
    except Exception as e: # Shouldn't be reached
        print e
        raise

    Block.objects.build_default() # JIC

    response_data = {
        'width' : stage.width,
        'height': stage.height,
        'spsize': 50,
        'start' : {'x': 0, 'y': 0, 'ID': Block.startID}, # Only one start point
        'end'   : {'x': 0, 'y': 0, 'ID': Block.endID}, # Only one end point for now
        'assets': {},
        'blocks': [],
    }
    assets = set() # For quicker access than re-iterating through an array
    x, y = 0, 0
    for c in stage.data:
        if c == '\r': 
            pass
        elif c == '\n':
            x, y = 0, y+1
        else:
            try:
                block = Block.objects.get(ID=c)
                if block.ID not in assets:
                    assets.add(block.ID)
                    response_data['assets'][block.ID] = block.sprite
                if block.ID == Block.startID:
                    response_data['start'] = {'x': x, 'y': y, 'ID': Block.startID}
                elif block.ID == Block.endID:
                    response_data['end'] = {'x': x, 'y': y, 'ID': Block.endID}
                else:
                    response_data['blocks'].append({'ID': block.ID, 'x': x, 'y': y})
            except ObjectDoesNotExist:
                pass
            x += 1

    return HttpResponse(json.dumps(response_data), content_type = 'application/json')

def get_stage(request):
    context = {}
    if request.user.is_authenticated():
        context['logged_in'] = True
        stages = Stage.objects.filter(owner = request.user.username)
        if stages:
            context['stages'] = stages
            sorted(context['stages'], key=lambda Stage: Stage.rating)
            context['message'] = "Choose one of your stages:"
        else:
            context['message'] = "You have no saved stages."
    else:
        context['message'] = 'You are not logged in!'
    return render(request, 'game/play.html', context)