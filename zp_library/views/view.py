from django.views.generic import View
from django.http import HttpResponseRedirect, HttpResponse

from zp_library.api import library_search, auth
from zp_library.models import *
from zp_library.forms import ISBNForm


class BookDeleteView(View):
    def dispatch(self, request, *args, **kwargs):
        library_user = auth.get_library_user()
        isbn = request.GET.get('isbn')

        if not library_user:
            return HttpResponseRedirect(auth.get_login_url('/book_delete'))

        if not library_user.type == auth.USER_TYPE_ADMIN:
            return HttpResponse(status=401)

        if library_user.type == auth.USER_TYPE_ADMIN:
            book_key = ndb.Key(Book, isbn)
            library_search.delete_book(book_key.get())
            book_key.delete()
            return HttpResponseRedirect('/book_list')

        return super(BookDeleteView, self).dispatch(request, *args, **kwargs)


class BookAddView(View):
    def dispatch(self, request, *args, **kwargs):
        library_user = auth.get_library_user()
        isbn = request.GET.get('isbn')

        if not library_user:
            return HttpResponseRedirect(auth.get_login_url('/'))

        if not library_user.type == auth.USER_TYPE_ADMIN:
            return HttpResponse(status=401)

        if library_user.type == auth.USER_TYPE_ADMIN:
            data = {
                "isbn_input": isbn
            }
            form = ISBNForm(data)

            form.action()
            return HttpResponseRedirect('/book_detail/?isbn=' + isbn)

        return super(BookAddView, self).dispatch(request, *args, **kwargs)

