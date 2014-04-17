from django.conf import settings
from django.conf.urls import patterns, include, url


from game import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pdm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^game\.html$', views.play_game, name='play_game'),
    url(r'^load/(?P<stage_id>\d+)/$', views.load_stage, name='load_stage'),
    url(r'^$', views.get_stage, name='get_stage'),
)
