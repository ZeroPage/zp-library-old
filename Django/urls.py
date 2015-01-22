from django.conf.urls import *

urlpatterns = patterns('',
    (r'^guestbook/', include('guestbook.urls')),
    (r'^', include('zp_library.urls')),
)