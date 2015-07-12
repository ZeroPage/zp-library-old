# coding=utf-8
from django.views.generic import *
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse

from zp_library.forms import *
from zp_library.models import *
from zp_library.views.view import LibraryView
from zp_library.api import extra_variable


class LibraryFormView(FormView, LibraryView):
    template_name = 'zp_library/form.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(LibraryFormView, self).get_context_data(**kwargs)

        try:
            context['site_name'] = extra_variable.get_extra_variable(extra_variable.SITE_NAME)
        except extra_variable.ExtraVariableKeyError:
            pass

        context['library_user'] = self.library_user
        context['google_user'] = self.google_user

        context['login_url'] = auth.get_login_url()
        context['logout_url'] = auth.get_logout_url()

        context['form_title'] = ''
        context['form_desc'] = ''

        return context


class BookAddISBNView(LibraryFormView):
    template_name = 'zp_library/form.html'
    form_class = ISBNForm
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if not self.library_user:
            return HttpResponseRedirect(auth.get_login_url('/add_isbn'))

        if not self.library_user.type == auth.USER_TYPE_ADMIN:
            return HttpResponse(status=401)

        return super(BookAddISBNView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BookAddISBNView, self).get_context_data(**kwargs)
        context['form_title'] = 'Add by ISBN'
        context['form_desc'] = 'ISBN을 이용해 책들을 추가할 수 있습니다. ISBN의 구분은 엔터를 이용합니다.'
        return context

    def form_valid(self, form):
        form.action()

        messages.success(self.request, 'added {} book(s)'.format(form.total_count))

        return super(BookAddISBNView, self).form_valid(form)


class SignUpView(LibraryFormView):
    template_name = 'zp_library/form.html'
    form_class = NewUserForm
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if self.library_user:
            return HttpResponseRedirect('/')

        if not self.google_user:
            return HttpResponseRedirect(auth.get_login_url())

        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        context['form_title'] = 'Sign up as ' + auth.get_google_user().email()
        context['form_desc'] = 'You need to signup to use this service.'
        return context

    def form_valid(self, form):
        form.action()

        messages.success(self.request, 'sign up complete. welcome.')

        return super(SignUpView, self).form_valid(form)


class BookEditView(LibraryFormView):
    template_name = 'zp_library/form.html'
    form_class = BookEditForm
    success_url = '/'
    isbn = ''

    def dispatch(self, request, *args, **kwargs):
        self.isbn = request.GET.get('isbn')

        if not self.library_user:
            return HttpResponseRedirect(auth.get_login_url('/book_edit'))

        if not self.library_user.type == auth.USER_TYPE_ADMIN:
            return HttpResponse(status=401)

        self.success_url = '/book_detail/?isbn='+self.isbn
        return super(BookEditView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(BookEditView, self).get_initial()

        book = ndb.Key(Book, self.isbn).get()

        initial['ISBN'] = book.ISBN
        initial['title'] = book.title
        initial['author'] = book.author
        initial['translator'] = book.translator
        initial['publisher'] = book.publisher
        initial['publishedDate'] = book.publishedDate
        initial['description'] = book.description
        initial['category'] = book.category
        initial['language'] = book.language
        initial['smallThumbnail'] = book.smallThumbnail
        initial['thumbnail'] = book.thumbnail
        initial['pageCount'] = book.pageCount
        initial['bookCount'] = book.bookCount
        initial['donor'] = book.donor

        return initial

    def form_valid(self, form):
        form.action()

        messages.success(self.request, 'edited book.')

        return super(BookEditView, self).form_valid(form)


class BookAddView(LibraryFormView):
    template_name = 'zp_library/form.html'
    form_class = BookForm
    success_url = '/book_list/'

    def dispatch(self, request, *args, **kwargs):
        if not self.library_user:
            return HttpResponseRedirect(auth.get_login_url('/test'))

        if not self.library_user.type == auth.USER_TYPE_ADMIN:
            return HttpResponse(status=401)

        return super(BookAddView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.action()

        messages.success(self.request, 'added new book.')

        return super(BookAddView, self).form_valid(form)

class ExtraVariableView(LibraryFormView):
    template_name = 'zp_library/form.html'
    form_class = ExtraVariableForm
    success_url = '/extra_variable/'

    def dispatch(self, request, *args, **kwargs):
        if not self.library_user:
            return HttpResponseRedirect(auth.get_login_url('/extra_variable/'))

        if not self.library_user.type == auth.USER_TYPE_ADMIN:
            return HttpResponse(status=401)

        return super(ExtraVariableView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ExtraVariableView, self).get_context_data(**kwargs)

        desc_str = ''

        for key in key_list:
            desc_str += key + ': '

            try:
                desc_str += get_extra_variable(key)
            except(ExtraVariableKeyError):
                pass

            desc_str += '\n'

        context['form_desc'] = desc_str
        return context

    def form_valid(self, form):
        form.action()

        messages.success(self.request, 'changed "{}" to "{}".'.format(form.cleaned_data['key'], form.cleaned_data['value']))

        return super(ExtraVariableView, self).form_valid(form)

class AddNoticeView(FormView):
    template_name = 'zp_library/form_notice.html'
    form_class = NoticeForm
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        library_user = auth.get_library_user()
        if not library_user:
            return HttpResponseRedirect(auth.get_login_url('/notice'))

        if not library_user.type == auth.USER_TYPE_ADMIN:
            return HttpResponse(status=401)
        return super(AddNoticeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddNoticeView, self).get_context_data(**kwargs)
        context['list'] = notice.get_notice()

        return context

    def form_valid(self, form):
        form.action()

        messages.success(self.request, 'added new notice.')

        return super(AddNoticeView, self).form_valid(form)
