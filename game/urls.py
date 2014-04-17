from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from game import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pdm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^game\.html$', views.play_game, name='play_game'),
    url(r'^load/(?P<stage_id>\d+)/$', views.load_stage, name='load_stage'),
    url(r'^$', views.get_stage, name='get_stage'),

    # http://docs.djangoproject.com/en/dev/howto/static-files/
    # This method is inefficient and insecure. 
    # Do not use this in a production setting. 
    # Use this only for development.
) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
