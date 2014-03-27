from django.conf.urls import patterns, include, url

from django.contrib import admin
#from users.views import HandlerView
from users.views import ResetView
from users.views import TestView

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', include('static_pages.urls')),
    url(r'^static_pages/', include('static_pages.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^game/', include('game.urls')), 

    #url(r'^client.html$', HandlerView.as_view(), name='my-view'),
    #url(r'^client.js$', HandlerView.as_view(), name='my-view'),
    #url(r'^client.css$', HandlerView.as_view(), name='my-view'),
    url(r'^login/', include('users.urls', namespace = 'users')),

    url(r'^stage/', include('stage.urls')),
    url(r'^assets/', 'static_pages.views.static_asset'),
) 
