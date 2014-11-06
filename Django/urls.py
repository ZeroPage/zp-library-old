from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^guestbook/', include('guestbook.urls')),
    (r'^', include('zp_library.urls')),
)