# coding=utf-8
import urllib2
import json
import math

from django.views.generic import *
from django.http import HttpResponseRedirect
from django.contrib import messages

from zp_library.api import auth, borrow, book, extra_variable, notice
from zp_library.models import *
from zp_library.views.view import LibraryView


class LibraryTemplateView(TemplateView, LibraryView):
    template_name = 'zp_library/base.html'

    def get_context_data(self, **kwargs):
        context = super(LibraryTemplateView, self).get_context_data(**kwargs)

        try:
            context['site_name'] = extra_variable.get_extra_variable(extra_variable.SITE_NAME)
        except extra_variable.ExtraVariableKeyError:
            pass

        context['library_user'] = self.library_user
        context['google_user'] = self.google_user

        context['login_url'] = auth.get_login_url()
        context['logout_url'] = auth.get_logout_url()

        return context


class MainPageView(LibraryTemplateView):
    template_name = 'zp_library/main.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.library_user:
            messages.info(request, 'Under Development!')

        return super(MainPageView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)

        # notice
        notice_result = notice.get_notice(1)

        if notice_result:
            context['message'] = notice_result[0]

        # borrow history

        borrow_records = borrow.get_borrows()[:5]  # fixme: limit needed
        borrow_refined = []

        for borrow_record in borrow_records:
            new_borrow = {
                'title': book.get_book(borrow_record.ISBN).title,
                'user_name': auth.get_library_user(borrow_record.userID).name,
                'ISBN': borrow_record.ISBN,
                'borrowDate': borrow_record.borrowDate,
                'returnDate': borrow_record.returnDate
            }

            borrow_refined.append(new_borrow)

        context['borrows'] = borrow_refined
        context['new_books'] = book.get_books(limit=5, sort=-Book.registrationDate)

        return context


class UserView(LibraryTemplateView):
    template_name = 'zp_library/user.html'

    def dispatch(self, request, *args, **kwargs):

        if not self.library_user:
            return HttpResponseRedirect(auth.get_login_url('/user'))

        return super(UserView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)

        borrow_records = borrow.get_borrows(user_id=self.library_user.id)
        borrow_refined = []

        for borrow_record in borrow_records:
            new_borrow = {}
            new_borrow['title'] = book.get_book(borrow_record.ISBN).title
            new_borrow['ISBN'] = borrow_record.ISBN
            new_borrow['borrowDate'] = borrow_record.borrowDate
            new_borrow['returnDate'] = borrow_record.returnDate

            borrow_refined.append(new_borrow)

        context['borrows'] = borrow_refined

        return context


class BookListView(LibraryTemplateView):
    template_name = 'zp_library/list.html'
    current_page = 1
    paginate_by = 10
    query_string = ''

    def dispatch(self, request, *args, **kwargs):
        self.current_page = int(request.GET.get('page') or 1)
        self.query_string = request.GET.get('q')

        return super(BookListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)

        if self.query_string:
            context['list_title'] = "Search result for '" + self.query_string + "'"
            search_results = library_search.search_book(self.query_string)

            search_isbn = []
            for result in search_results.results:
                search_isbn.append(result.doc_id)

            if not search_isbn:
                search_isbn = ['-']

        else:
            context['list_title'] = 'All books'
            search_isbn = []

        context['books'] = book.get_books((self.current_page - 1) * self.paginate_by, self.paginate_by, search_isbn)

        if context['books']:
            context['page_range'] = range(1, int(math.ceil(book.get_books_count() / self.paginate_by)) + 1)
            context['page'] = self.current_page
            context['is_first'] = self.current_page == context['page_range'][0]
            context['is_last'] = self.current_page == context['page_range'][-1]
            context['no_img_url'] = "/static/img/no_image.png"

        return context


class BookDetailView(LibraryTemplateView):
    template_name = 'zp_library/detail.html'
    isbn = ''

    def dispatch(self, request, *args, **kwargs):
        self.isbn = request.GET.get('isbn')

        return super(BookDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)

        book_result = book.get_book(self.isbn)
        raw_borrows = borrow.get_borrows(self.isbn)

        borrows = []

        for borrow_record in raw_borrows:
            borrower = auth.get_library_user(borrow_record.userID)

            borrows.append({
                'name': borrower.name,
                'borrowDate': borrow_record.borrowDate,
                'returnDate': borrow_record.returnDate,
            })

        context['borrows'] = borrows

        if book_result:
            context['book'] = book_result

            basic_info = dict()
            context['basic_info'] = basic_info
            if book_result.translator:
                basic_info['번역자'] = book_result.translator

            if book_result.publisher:
                basic_info['출판사'] = book_result.publisher

            if book_result.category:
                basic_info['카테고리'] = book_result.category

            if book_result.language:
                basic_info['언어'] = book_result.language

            if book_result.pageCount:
                basic_info['페이지'] = book_result.pageCount

            if book_result.publishedDate:
                basic_info['출판일'] = book_result.publishedDate

            extra_info = dict()
            context['extra_info'] = extra_info
            if book_result.bookCount:
                extra_info['책 보유수'] = book_result.bookCount

            if book_result.donor:
                extra_info['기증자'] = book_result.donor

            if book_result.registrationDate:
                extra_info['등록일자'] = book_result.registrationDate

        context['isbn'] = self.isbn

        return context

class BarcodeView(LibraryTemplateView):
    template_name = 'zp_library/barcode.html'
