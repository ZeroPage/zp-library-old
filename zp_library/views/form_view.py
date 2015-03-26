from django.views.generic import *
from django.http import HttpResponseRedirect, HttpResponse

from zp_library.forms import *
from zp_library.models import *


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

    def get_context_data(self, **kwargs):
        context = super(ISBNAddView, self).get_context_data(**kwargs)
        context['form_title'] = 'test'
        return context

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

        if not auth.get_google_user():
            return HttpResponseRedirect(auth.get_login_url())

        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        context['form_title'] = 'Sign up as ' + auth.get_google_user().email()
        context['form_desc'] = 'You need to signup to use this service.'
        return context

    def form_valid(self, form):
        form.action()

        return super(SignUpView, self).form_valid(form)


class BookEditView(FormView):
    template_name = 'zp_library/form.html'
    form_class = BookEditForm
    success_url = '/'
    isbn = ''

    def dispatch(self, request, *args, **kwargs):
        library_user = auth.get_library_user()
        self.isbn = request.GET.get('isbn')

        if not library_user:
            return HttpResponseRedirect(auth.get_login_url('/book_edit'))

        if not library_user.type == auth.USER_TYPE_ADMIN:
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

        return super(BookEditView, self).form_valid(form)


class TestView(FormView):
    template_name = 'zp_library/form.html'
    form_class = BookForm
    success_url = '/book_list/'

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