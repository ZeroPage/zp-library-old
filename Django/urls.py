from django.conf.urls import *

urlpatterns = patterns('',
    (r'^', include('zp_library.urls'))
)