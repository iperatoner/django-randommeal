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
        r'^all-meals/$',
        views.all_meals,
        name='rdm_all'
    ),
    
    url(
        r'^print-meal/(?P<meal_id>[0-9]+)/$',
        views.print_meal,
        name='rdm_print_meal'
    ),
    
    url(
        r'^have-eaten/(?P<meal_id>[0-9]+)/(?P<redirect>[a-z]+)/$',
        views.have_eaten,
        name='rdm_have_eaten'
    ),
)
