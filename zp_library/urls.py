from django.conf.urls import *
from zp_library.views import *

urlpatterns = [
    url(r'^$', template_view.MainPageView.as_view(), name='main'),
    url(r'^user/$', template_view.UserView.as_view(), name='user'),
    url(r'^test/$', form_view.TestView.as_view(), name='test'),
    url(r'^book_list/$', template_view.BookListView.as_view(), name='book_list'),
    url(r'^add_isbn/$', form_view.ISBNAddView.as_view(), name='add_isbn'),
    url(r'^book_detail/$', template_view.BookDetailView.as_view(), name='book_detail'),
    url(r'^book_edit/$', form_view.BookEditView.as_view(), name='book_edit'),
    url(r'^book_delete/$', view.BookDeleteView.as_view(), name='book_delete'),
    url(r'^parse/$', template_view.ParseView.as_view()),
    url(r'^signup/$', form_view.SignUpView.as_view()),
    url(r'^barcode/$', template_view.BarcodeView.as_view(), name='barcode')
]