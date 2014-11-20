from django.conf.urls.defaults import *
from zp_library.views import *

urlpatterns = [
	url(r'^$', MainPageView.as_view(), name='main'),
	url(r'^test/$', TestView.as_view(), name='test'),
	url(r'^parse/$', ParseView.as_view())
]