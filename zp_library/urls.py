from django.conf.urls.defaults import *
from zp_library.views import main_page, parse_book

urlpatterns = patterns('',
    (r'^$', main_page),
    (r'^parse/$', parse_book),
)