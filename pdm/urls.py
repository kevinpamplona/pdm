from django.conf.urls import patterns, include, url

from django.contrib import admin
from users.views import HandlerView
from users.views import ResetView
from users.views import TestView

from stage.views import RenderView
from stage.views import EditorView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pdm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^game/', include('game.urls')),    
    url(r'^users/login$', HandlerView.as_view(), name='my-view'),
    url(r'^users/add$', HandlerView.as_view(), name='my-view'),
    url(r'^TESTAPI/resetFixture$', ResetView.as_view(), name='reset-view'),
    url(r'^TESTAPI/unitTests$', TestView.as_view(), name='test-view'),
    url(r'^client.html$', HandlerView.as_view(), name='my-view'),
    url(r'^client.js$', HandlerView.as_view(), name='my-view'),
    url(r'^client.css$', HandlerView.as_view(), name='my-view'),
    url(r'^stage/render$', RenderView.as_view(), name='my-view'),
    url(r'^editor.html$', EditorView.as_view(), name='my-view'),
    url(r'^style.css$', EditorView.as_view(), name='my-view'),

) 
