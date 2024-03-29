from google.appengine.api import users

from django import forms
from zp_library.models import *
from zp_library.api import book_api, auth, notice
from zp_library.api.extra_variable import *


class BookForm(forms.Form):
    ISBN = forms.CharField()
    title = forms.CharField()
    author = forms.CharField()
    translator = forms.CharField(required=False)
    publisher = forms.CharField(required=False)
    publishedDate = forms.DateField(required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    category = forms.CharField(required=False)
    language = forms.CharField(required=False)
    smallThumbnail = forms.CharField(required=False)
    thumbnail = forms.CharField(required=False)
    pageCount = forms.IntegerField(required=False)
    bookCount = forms.IntegerField(required=False)
    donor = forms.CharField(required=False)

    def action(self):
        if self.is_valid():
            book = Book()

            book.ISBN = self.cleaned_data['ISBN']
            book.title = self.cleaned_data['title']
            book.author = self.cleaned_data['author']
            book.translator = self.cleaned_data['translator']
            book.publisher = self.cleaned_data['publisher']
            book.publishedDate = self.cleaned_data['publishedDate']
            book.description = self.cleaned_data['description']
            book.category = self.cleaned_data['category']
            book.language = self.cleaned_data['language']
            book.smallThumbnail = self.cleaned_data['smallThumbnail']
            book.thumbnail = self.cleaned_data['thumbnail']
            book.pageCount = self.cleaned_data['pageCount']
            if not self.cleaned_data['bookCount']:
                book.bookCount = 1
            else:
                book.bookCount = self.cleaned_data['bookCount']
            book.donor = self.cleaned_data['donor']
            book.key = ndb.Key(Book, self.cleaned_data['ISBN'])

            book.put()


class BookEditForm(BookForm):
    ISBN = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def action(self):
        if self.is_valid():
            book = ndb.Key(Book, self.cleaned_data['ISBN']).get()

            book.title = self.cleaned_data['title']
            book.author = self.cleaned_data['author']
            book.translator = self.cleaned_data['translator']
            book.publisher = self.cleaned_data['publisher']
            book.publishedDate = self.cleaned_data['publishedDate']
            book.description = self.cleaned_data['description']
            book.category = self.cleaned_data['category']
            book.language = self.cleaned_data['language']
            book.smallThumbnail = self.cleaned_data['smallThumbnail']
            book.thumbnail = self.cleaned_data['thumbnail']
            book.pageCount = self.cleaned_data['pageCount']
            if not self.cleaned_data['bookCount']:
                book.bookCount = 1
            else:
                book.bookCount = self.cleaned_data['bookCount']
            book.donor = self.cleaned_data['donor']

            book.put()

class ISBNForm(forms.Form):
    isbn_input = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'multiple items allowed (split by enter)'}))
    total_count = 0

    def action(self):
        if self.is_valid():
            isbns = self.cleaned_data["isbn_input"].split()
            google = book_api.Google(get_extra_variable(GOOGLE_BOOK_API_KEY))
            daum = book_api.Daum(get_extra_variable(DAUM_BOOK_API_KEY))

            for isbn in isbns:
                request_parameters = {
                    "isbn": isbn
                }
                google.request(request_parameters)
                daum.request(request_parameters)

                google.filter()
                daum.filter()

                data = book_api.selectBookData(google.result, daum.result)

                book_form = BookForm(data)
                book_form.action()

                self.total_count += 1


class NewUserForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'type real name'}))

    def action(self):
        if self.is_valid():
            auth.add_user(self.cleaned_data['name'])


class NoticeForm(forms.Form):
    contents = forms.CharField(widget=forms.TextInput)

    def action(self):
        if self.is_valid():
            notice.add_notice(self.cleaned_data['contents'])

class ExtraVariableForm(forms.Form):
    key = forms.CharField(widget=forms.TextInput)
    value = forms.CharField(widget=forms.TextInput)

    def action(self):
        if self.is_valid():
            set_extra_variable(self.cleaned_data['key'], self.cleaned_data['value'])