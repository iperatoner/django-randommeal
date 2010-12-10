from django.conf.urls.defaults import *
from . import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='rdm_index'),
    
    url(
        r'^generate/$',
        views.generate,
        name='rdm_generate'
    ),
)
