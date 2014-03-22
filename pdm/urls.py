from django.conf.urls import patterns, include, url

from django.contrib import admin
from users.views import HandlerView
from users.views import ResetView
from users.views import TestView

from stage.views import RenderView
from stage.views import EditorView
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', include('static_pages.urls')),
    url(r'^static_pages/', include('static_pages.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^game/', include('game.urls')),    
    url(r'^client.html$', HandlerView.as_view(), name='my-view'),
    url(r'^client.js$', HandlerView.as_view(), name='my-view'),
    url(r'^client.css$', HandlerView.as_view(), name='my-view'),

    url(r'^stage/', include('stage.urls')),
    url(r'^style.css$', EditorView.as_view(), name='my-view'),

) 
