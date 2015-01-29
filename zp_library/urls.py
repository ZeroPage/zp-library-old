from django.conf.urls import *
from zp_library.views import *

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='main'),
    url(r'^admin/$', AdminView.as_view(), name='admin'),
    url(r'^test/$', TestView.as_view(), name='test'),
    url(r'^book_list/$', BookListView.as_view(), name='book_list'),
    url(r'^add_isbn/$', ISBNAddView.as_view(), name='add_isbn'),
    url(r'^book_detail/$', BookDetailView.as_view(), name='book_detail'),
    url(r'^parse/$', ParseView.as_view())
]