from django.conf.urls import patterns, url

from users import views

urlpatterns = patterns('',
	url(r'^search$', views.search, name='search'),
    url(r'^/?$', views.get_login, name='login'),
)