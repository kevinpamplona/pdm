from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
#from users.views import HandlerView
from users.views import ResetView
from users.views import TestView

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', include('static_pages.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^game/', include('game.urls', namespace = 'game')), 

    url(r'^login/', include('users.urls', namespace = 'users')),

    url(r'^stage/', include('stage.urls', namespace = 'stage')),
    url(r'^assets/', 'static_pages.views.static_asset'),
)
