# coding=utf-8
from django.views.generic import *
from django.http import HttpResponseRedirect
from zp_library.forms import *
from google.appengine.api import users
from zp_library.models import *

import urllib2
import json


class MainPageView(TemplateView):
    template_name = 'zp_library/main_page.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['message'] = '지피 도서관에 어서오세요'

        return context


class AdminView(TemplateView):
    template_name = 'zp_library/admin_page.html'

    def dispatch(self, request, *args, **kwargs):
        if not users.get_current_user():
            return HttpResponseRedirect(users.create_login_url('/admin'))

        return super(AdminView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AdminView, self).get_context_data(**kwargs)

        user = users.get_current_user()

        context['is_admin'] = users.is_current_user_admin()
        context['logout_url'] = users.create_logout_url('/')
        context['user'] = user

        return context


class TestView(FormView):
    template_name = 'zp_library/form.html'
    form_class = BookForm
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if not users.is_current_user_admin():
            return HttpResponseRedirect('/')

        return super(TestView, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        cleaned_data = form.action()
        book = Book(parent=book_key())

        book.ISBN = cleaned_data['ISBN']
        book.title = cleaned_data['title']
        book.author = cleaned_data['author']
        book.translator = cleaned_data['translator']
        book.publisher = cleaned_data['publisher']
        book.publishedDate = cleaned_data['publishedDate']
        book.description = cleaned_data['description']
        book.category = cleaned_data['category']
        book.language = cleaned_data['language']
        book.smallThumbnail = cleaned_data['smallThumbnail']
        book.thumbnail = cleaned_data['thumbnail']
        book.pageCount = cleaned_data['pageCount']
        book.bookCount = cleaned_data['bookCount']
        book.donor = cleaned_data['donor']
        book.put()
        return super(TestView, self).form_valid(form)


class BookListView(TemplateView):
    template_name = 'zp_library/list.html'

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)

        books_query = Book.query(ancestor=book_key()).order(Book.title)
        context['books'] = books_query.fetch(10)

        return context

class BookDetailView(TemplateView):
    template_name = 'zp_library/detail.html'
    isbn = ''

    def dispatch(self, request, *args, **kwargs):
        self.isbn = request.GET.get('isbn')

        return super(BookDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)

        books_query = Book.query(Book.ISBN == self.isbn)
        context['books'] = books_query.fetch()

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
