# coding=utf-8
from django.views.generic import *
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from zp_library.forms import *
from zp_library.models import *
from zp_library import auth

import urllib2
import json


class MainPageView(TemplateView):
    template_name = 'zp_library/main_page.html'

    def dispatch(self, request, *args, **kwargs):
        return super(MainPageView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['message'] = '지피 도서관에 어서오세요.'

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


class TestView(FormView):
    template_name = 'zp_library/form.html'
    form_class = BookForm
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        library_user = auth.get_library_user()
        if not library_user:
            return HttpResponseRedirect(auth.get_login_url('/test'))

        if not library_user.type == auth.USER_TYPE_ADMIN:
            return HttpResponse(status=401)

        return super(TestView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.action()

        return super(TestView, self).form_valid(form)


class BookListView(TemplateView):
    template_name = 'zp_library/list.html'
    current_page = 1
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        self.current_page = request.GET.get('page')

        return super(BookListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)

        books_query = Book.query(ancestor=book_key()).order(Book.title)
        paginator = Paginator(books_query.fetch(), self.paginate_by)

        try:
            context['books'] = paginator.page(self.current_page)
        except (PageNotAnInteger, EmptyPage):
            context['books'] = paginator.page(1)

        context['page_range'] = range(1, paginator.num_pages + 1)
        context['is_first'] = self.current_page == 1
        context['is_last'] = self.current_page == paginator.num_pages

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


class CameraView(TemplateView):
    template_name = 'zp_library/camera.html'

    def dispatch(self, request, *args, **kwargs):
        return super(CameraView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CameraView, self).get_context_data(**kwargs)

        return context


class ISBNAddView(FormView):
    template_name = 'zp_library/form.html'
    form_class = ISBNForm
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        library_user = auth.get_library_user()
        if not library_user:
            return HttpResponseRedirect(auth.get_login_url('/add_isbn'))

        if not library_user.type == auth.USER_TYPE_ADMIN:
            return HttpResponse(status=401)

        return super(ISBNAddView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.action()

        return super(ISBNAddView, self).form_valid(form)


class SignUpView(FormView):
    template_name = 'zp_library/form.html'
    form_class = NewUserForm
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        library_user = auth.get_library_user()

        if library_user:
            return HttpResponseRedirect('/')

        if not auth.get_google_id():
            return HttpResponseRedirect(auth.get_login_url())

        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.action()

        return super(SignUpView, self).form_valid(form)
