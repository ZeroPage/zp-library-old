from google.appengine.api import users

from django import forms
from zp_library.models import *
from zp_library.api import book_api, auth


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

    def action(self):
        if self.is_valid():
            isbns = self.cleaned_data["isbn_input"].split()
            google = book_api.Google()
            daum = book_api.Daum()

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


class NewUserForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'type real name'}))

    def action(self):
        google_user = users.get_current_user()

        if self.is_valid() and google_user and not LibraryUser.query(LibraryUser.id == google_user.user_id()).get():
            if users.is_current_user_admin():
                user_type = auth.USER_TYPE_ADMIN
            else:
                user_type = auth.USER_TYPE_NEW

            LibraryUser(id=google_user.user_id(), email=google_user.email(),
                        name=self.cleaned_data['name'], type=user_type).put()


class NoticeForm(forms.Form):
    contents = forms.CharField(widget=forms.TextInput)

    def action(self):
        if self.is_valid():
            notice = Notice()

            notice.contents = self.cleaned_data['contents']
            notice.put()