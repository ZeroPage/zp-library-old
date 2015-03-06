from django.conf.urls import *
from zp_library.views import *

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='main'),
    url(r'^user/$', UserView.as_view(), name='user'),
    url(r'^test/$', TestView.as_view(), name='test'),
    url(r'^book_list/$', BookListView.as_view(), name='book_list'),
    url(r'^add_isbn/$', ISBNAddView.as_view(), name='add_isbn'),
    url(r'^book_detail/$', BookDetailView.as_view(), name='book_detail'),
    url(r'^book_delete/$', BookDeleteView.as_view(), name='book_delete'),
    url(r'^parse/$', ParseView.as_view()),
    url(r'^signup/$', SignUpView.as_view()),
    url(r'^camera/$', CameraView.as_view(), name='camera')
]