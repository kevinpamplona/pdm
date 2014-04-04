from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from views import HandlerView
from game import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pdm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'\.(html|css|js)$', HandlerView.as_view(), name = 'get-page'),
    url(r'^(?P<stage_id>\d+)\.json$', views.load_stage, name='load_stage'),
    url(r'^\.json$', views.load_stage, name='load_stage'),
    url(r'^$', views.get_stage, name='get_stage'),

    # http://docs.djangoproject.com/en/dev/howto/static-files/
    # This method is inefficient and insecure. 
    # Do not use this in a production setting. 
    # Use this only for development.
) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
