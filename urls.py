from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

import settings

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    
    (r'^', include('meals.urls')),
    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT, 
        'show_indexes': True 
    })
)
