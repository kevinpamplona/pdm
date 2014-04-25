from django.conf.urls import patterns, url

from users import views

urlpatterns = patterns('',
    url(r'^/?$', views.get_login, name='login'),
)