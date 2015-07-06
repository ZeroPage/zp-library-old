from django.conf.urls import *
from zp_library.views import view, template_view, form_view

urlpatterns = [
    url(r'^$', template_view.MainPageView.as_view(), name='main'),
    url(r'^user/$', template_view.UserView.as_view(), name='user'),
    url(r'^book_list/$', template_view.BookListView.as_view(), name='book_list'),
    url(r'^book_detail/$', template_view.BookDetailView.as_view(), name='book_detail'),
    url(r'^barcode/$', template_view.BarcodeView.as_view(), name='barcode'),

    url(r'^book_add/$', form_view.BookAddView.as_view(), name='book_add'),
    url(r'^book_edit/$', form_view.BookEditView.as_view(), name='book_edit'),
    url(r'^book_add_isbn/$', form_view.BookAddISBNView.as_view(), name='book_add_isbn'),
    url(r'^signup/$', form_view.SignUpView.as_view(), name='signup'),
    url(r'^notice/$', form_view.AddNoticeView.as_view(), name='notice'),
    url(r'^extra_variable/$', form_view.ExtraVariableView.as_view(), name='extra_variable'),

    url(r'^book_delete/$', view.BookDeleteView.as_view(), name='book_delete'),
    url(r'^book_add/$', view.BookAddView.as_view(), name='book_add'),
    url(r'^book_update_all/$', view.UpdateAllView.as_view(), name='book_update_all'),
    url(r'^book_borrow/$', view.BookBorrowView.as_view(), name='book_borrow'),
]