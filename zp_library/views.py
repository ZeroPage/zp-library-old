from django.views.generic import *
from zp_library.forms import *
from google.appengine.api import users
from zp_library.models import *

import urllib2
import json


class MainPageView(TemplateView):
    template_name = 'zp_library/main_page.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['message'] = 'test'

        context['user'] = users.get_current_user()
        context['logged_in'] = bool(context['user'])
        context['login_url'] = users.create_login_url()
        context['logout_url'] = users.create_logout_url('/')

        return context


class TestView(FormView):
    template_name = 'zp_library/form.html'
    form_class = BookForm
    success_url = '/'

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

        books_query = Book.query(ancestor=book_key()).order(-Book.registrationDate)
        context['books'] = books_query.fetch(10)

        return context


class ParseView(TemplateView):
    template_name = 'zp_library/parse.html'

    def get_context_data(self, **kwargs):
        context = super(ParseView, self).get_context_data(**kwargs)

        isbn = '9788966260546'
        #isbn = request.GET.get('isbn', '9788966260546')
        json_result = json.load(urllib2.urlopen('https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn))

        context['result'] = json.dumps(json_result, indent=4, ensure_ascii=False, separators=(',', ': '))

        return context