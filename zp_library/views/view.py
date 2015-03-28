from django.views.generic import View
from django.http import HttpResponseRedirect, HttpResponse

from zp_library.api import auth
from zp_library.models import *
from zp_library.forms import ISBNForm


class LibraryView(View):
    @property
    def library_user(self):
	return auth.get_library_user()

    @property
    def google_user(self):
	return auth.get_google_user()


class BookDeleteView(LibraryView):
    def dispatch(self, request, *args, **kwargs):
        isbn = request.GET.get('isbn')

        if not self.library_user:
            return HttpResponseRedirect(auth.get_login_url('/book_delete'))

        if not self.library_user.type == auth.USER_TYPE_ADMIN:
            return HttpResponse(status=401)

        if self.library_user.type == auth.USER_TYPE_ADMIN:
            book_key = ndb.Key(Book, isbn)
            book_key.delete()
            return HttpResponseRedirect('/book_list')

        return super(BookDeleteView, self).dispatch(request, *args, **kwargs)


class BookAddView(LibraryView):
    def dispatch(self, request, *args, **kwargs):
        isbn = request.GET.get('isbn')

        if not self.library_user:
            return HttpResponseRedirect(auth.get_login_url('/'))

        if not self.library_user.type == auth.USER_TYPE_ADMIN:
            return HttpResponse(status=401)

        if self.library_user.type == auth.USER_TYPE_ADMIN:
            data = {
                "isbn_input": isbn
            }
            form = ISBNForm(data)

            form.action()
            return HttpResponseRedirect('/book_detail/?isbn=' + isbn)

        return super(BookAddView, self).dispatch(request, *args, **kwargs)


class UpdateAllView(LibraryView):
    def dispatch(self, request, *args, **kwargs):
        if not self.library_user:
            return HttpResponseRedirect(auth.get_login_url('/'))

        if not self.library_user.type == auth.USER_TYPE_ADMIN:
            return HttpResponse(status=401)

        if self.library_user.type == auth.USER_TYPE_ADMIN:
            books = Book.query().fetch()

            for book in books:
                data = {
                    "isbn_input": book.ISBN
                }
                form = ISBNForm(data)

                form.action()

            return HttpResponseRedirect('/book_list')

        return super(UpdateAllView, self).dispatch(request, *args, **kwargs)
