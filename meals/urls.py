from django.conf.urls.defaults import *
from . import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='rdm_index'),
    
    url(
        r'^generate/$',
        views.generate,
        name='rdm_generate'
    ),
    
    url(
        r'^have_eaten/(?P<meal_id>[0-9]+)/$',
        views.have_eaten,
        name='rdm_have_eaten'
    ),
)
