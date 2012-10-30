from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^', include('traveler.urls')),
    url(r'', include('social_auth.urls')),
)

