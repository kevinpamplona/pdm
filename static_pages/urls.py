from django.conf import settings
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'', 'static_pages.views.static_page', name='index')
)
