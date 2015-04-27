from django.views.generic import View
from django.http import HttpResponseRedirect, HttpResponse

from zp_library.api import auth
from zp_library.models import *
from zp_library.forms import ISBNForm

from datetime import datetime
import logging


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


class BookBorrowView(LibraryView):
    def dispatch(self, request, *args, **kwargs):
        isbn = request.GET.get('isbn')

        if not self.library_user:
            return HttpResponseRedirect(auth.get_login_url('/'))

        borrow_query = BookBorrow.query(BookBorrow.ISBN == isbn, BookBorrow.returnDate == None)
        my_borrow_query = borrow_query.filter(BookBorrow.userID == self.library_user.id)

        my_borrow_result = my_borrow_query.fetch()

        logging.info(my_borrow_result)

        if my_borrow_result:
            for borrow_record in my_borrow_result:
                borrow_record.returnDate = datetime.now()
                borrow_record.put()
        else:
            borrow_result = borrow_query.fetch()
            logging.info(borrow_result)


            book_result = Book.query(Book.ISBN == isbn).fetch(limit=1)[0]

            if book_result and len(borrow_result) < book_result.bookCount:
                new_borrow = BookBorrow()
                new_borrow.ISBN = isbn
                new_borrow.userID = self.library_user.id

                new_borrow.put()

        return HttpResponseRedirect('/book_detail/?isbn=' + isbn)


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
