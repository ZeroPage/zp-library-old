from django import forms
from zp_library.models import *

class BookForm(forms.Form):
    ISBN = forms.CharField()
    title = forms.CharField()
    author = forms.CharField()
    translator = forms.CharField()
    publisher = forms.CharField()
    publishedDate = forms.DateField()
    description = forms.CharField(widget=forms.Textarea)
    category = forms.CharField()
    language = forms.CharField()
    smallThumbnail = forms.CharField()
    thumbnail = forms.CharField()
    pageCount = forms.IntegerField()
    bookCount = forms.IntegerField()
    donor = forms.CharField(required=False)

    def action(self):
        if self.is_valid():
            book = Book(parent=book_key())

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
            book.bookCount = self.cleaned_data['bookCount']
            book.donor = self.cleaned_data['donor']
            book.put()


class ISBNForm(forms.Form):
    isbn = forms.CharField(widget=forms.Textarea)

    def action(self):
        if self.is_valid():
            isbns = self.cleaned_data['isbn'].splitlines()

            for isbn in isbns:
                data = {'ISBN': isbn,
                        'title': 'title',
                        'author': 'author',
                        'translator': 'trans',
                        'publisher': 'pub',
                        'publishedDate': '2000-1-1',
                        'description': 'a',
                        'category': 'cate',
                        'language': 'lang',
                        'smallThumbnail': 'small',
                        'thumbnail': 'thumb',
                        'pageCount': 3,
                        'bookCount': 1,
                        'donor': 'donor'}
                book_form = BookForm(data)
                book_form.action()
