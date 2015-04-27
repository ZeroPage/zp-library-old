from django.conf.urls import *
from zp_library.views import *

urlpatterns = [
    url(r'^$', template_view.MainPageView.as_view(), name='main'),
    url(r'^user/$', template_view.UserView.as_view(), name='user'),
    url(r'^book_list/$', template_view.BookListView.as_view(), name='book_list'),
    url(r'^book_detail/$', template_view.BookDetailView.as_view(), name='book_detail'),
    url(r'^parse/$', template_view.ParseView.as_view()),
    url(r'^barcode/$', template_view.BarcodeView.as_view(), name='barcode'),

    url(r'^test/$', form_view.TestView.as_view(), name='test'),
    url(r'^add_isbn/$', form_view.ISBNAddView.as_view(), name='add_isbn'),
    url(r'^book_edit/$', form_view.BookEditView.as_view(), name='book_edit'),
    url(r'^signup/$', form_view.SignUpView.as_view()),
    url(r'^notice/$', form_view.AddNoticeView.as_view(), name="notice"),

    url(r'^book_delete/$', view.BookDeleteView.as_view(), name='book_delete'),
    url(r'^book_add/$', view.BookAddView.as_view(), name="book_add"),
    url(r'^update_all/$', view.UpdateAllView.as_view(), name="update_all"),
    url(r'^book_borrow/$', view.BookBorrowView.as_view(), name="book_borrow"),
]