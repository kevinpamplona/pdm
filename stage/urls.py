from django.conf import settings
from django.conf.urls import patterns, include, url

from views import RenderView
from views import EditorView
from stage import views

urlpatterns = patterns('',

    url(r'^render$', RenderView.as_view(), name='render'),
    url(r'^editor$', EditorView.as_view(), name='editor'),

)
