# coding=utf-8
import urllib2
import json

from django.views.generic import *
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from zp_library.api import library_search, auth
from zp_library.models import *


class MainPageView(TemplateView):
    template_name = 'zp_library/main_page.html'

    def dispatch(self, request, *args, **kwargs):
        return super(MainPageView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)

        notice_query = Notice.query().order(-Notice.date)
        notice_result = notice_query.fetch(limit=1)

        if notice_result:
            context['message'] = notice_result[0]

        return context


class UserView(TemplateView):
    template_name = 'zp_library/user_page.html'

    def dispatch(self, request, *args, **kwargs):

        if not auth.get_library_user():
            return HttpResponseRedirect(auth.get_login_url('/user'))

        return super(UserView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)

        context['logout_url'] = auth.get_logout_url()
        context['library_user'] = auth.get_library_user()

        return context


class BookListView(TemplateView):
    template_name = 'zp_library/list.html'
    current_page = 1
    paginate_by = 10
    query_string = ''

    def dispatch(self, request, *args, **kwargs):
        self.current_page = request.GET.get('page')
        self.query_string = request.GET.get('q')

        return super(BookListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)

        context['library_user'] = auth.get_library_user()

        if self.query_string:
            context['list_title'] = "Search result for '" + self.query_string + "'"
            search_results = library_search.search_book(self.query_string)

            search_isbn = []
            for result in search_results.results:
                search_isbn.append(result.doc_id)

            if not search_isbn:
                search_isbn = ['-']

            books_query = Book.query(Book.ISBN.IN(search_isbn)).order(Book.title)
        else:
            context['list_title'] = 'All books'
            books_query = Book.query().order(Book.title)

        paginator = Paginator(books_query.fetch(), self.paginate_by)

        try:
            context['books'] = paginator.page(self.current_page)
        except (PageNotAnInteger, EmptyPage):
            context['books'] = paginator.page(1)

        context['page_range'] = range(1, paginator.num_pages + 1)
        context['is_first'] = self.current_page == 1
        context['is_last'] = self.current_page == paginator.num_pages

        context['no_img_url'] = "/static/img/no_image.png"

        return context


class BookDetailView(TemplateView):
    template_name = 'zp_library/detail.html'
    isbn = ''

    def dispatch(self, request, *args, **kwargs):
        self.isbn = request.GET.get('isbn')

        return super(BookDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)

        book_query = Book.query(Book.key == ndb.Key(Book, self.isbn))
        book_result = book_query.fetch(limit=1)

        if book_result:
            book_result = book_result[0]
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


class ParseView(TemplateView):
    template_name = 'zp_library/parse.html'
    isbn = ''

    def dispatch(self, request, *args, **kwargs):
        self.isbn = request.GET.get('isbn', '9788966260546')

        return super(ParseView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ParseView, self).get_context_data(**kwargs)

        try:
            json_result = json.load(urllib2.urlopen('https://www.googleapis.com/books/v1/volumes?'
                                                    + 'q=isbn:' + self.isbn
                                                    + '&key=AIzaSyCEFHrF-qRjKkh3p9hvOpY9lhzdOtsS0UE'
                                                    + '&country=KR'))
            context['result'] = json.dumps(json_result, indent=4, ensure_ascii=False, separators=(',', ': '))
        except urllib2.HTTPError, e:
            context['result'] = e.fp.read()

        return context


class BarcodeView(TemplateView):
    template_name = 'zp_library/barcode.html'

    def dispatch(self, request, *args, **kwargs):
        return super(BarcodeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BarcodeView, self).get_context_data(**kwargs)

        return context