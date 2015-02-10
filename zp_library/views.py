# coding=utf-8
from django.views.generic import *
from django.http import HttpResponseRedirect
from zp_library.forms import *
from google.appengine.api import users
from zp_library.models import *
from django.core.paginator import Paginator, PageNotAnInteger

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
        form.action()

        return super(TestView, self).form_valid(form)


class BookListView(TemplateView):
    template_name = 'zp_library/list.html'
    page = 1

    def dispatch(self, request, *args, **kwargs):
        self.page = request.GET.get('page')

        return super(BookListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)

        books_query = Book.query(ancestor=book_key()).order(Book.title)
        paginator = Paginator(books_query.fetch(), 10)

        try:
            context['books'] = paginator.page(self.page)
        except PageNotAnInteger:
            context['books'] = paginator.page(1)

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


class ISBNAddView(FormView):
    template_name = 'zp_library/form.html'
    form_class = ISBNForm
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if not users.get_current_user():
            return HttpResponseRedirect(users.create_login_url('/admin'))

        return super(ISBNAddView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.action()

        return super(ISBNAddView, self).form_valid(form)
