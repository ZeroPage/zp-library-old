from django.views.generic import *
from zp_library.forms import *

import urllib2
import json


class MainPageView(TemplateView):
    template_name = 'zp_library/main_page.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['message'] = 'test'

        return context


class TestView(FormView):
    template_name = 'zp_library/form.html'
    form_class = BookForm
    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        cleaned_data = form.action()
        book = Book(parent=book_key(cleaned_data['ISBN']))

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


class ParseView(TemplateView):
    template_name = 'zp_library/parse.html'

    def get_context_data(self, **kwargs):
        context = super(ParseView, self).get_context_data(**kwargs)

        isbn = '9788966260546'
        #isbn = request.GET.get('isbn', '9788966260546')
        json_result = json.load(urllib2.urlopen('https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn))

        context['result'] = json.dumps(json_result, indent=4, ensure_ascii=False, separators=(',', ': '))

        return context