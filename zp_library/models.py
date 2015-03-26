from google.appengine.ext import ndb
from zp_library.api import library_search

DEFAULT_BOOK_NAME = 'default_book'
DEFAULT_USER_KEY_NAME = 'default_user'


class Book(ndb.Model):
    ISBN = ndb.StringProperty()
    title = ndb.StringProperty()
    author = ndb.StringProperty()
    translator = ndb.StringProperty()
    publisher = ndb.StringProperty()
    publishedDate = ndb.DateProperty()
    description = ndb.TextProperty()
    category = ndb.StringProperty()
    language = ndb.StringProperty()
    smallThumbnail = ndb.StringProperty()
    thumbnail = ndb.StringProperty()
    pageCount = ndb.IntegerProperty()
    bookCount = ndb.IntegerProperty()
    donor = ndb.StringProperty()
    registrationDate = ndb.DateProperty(auto_now_add=True)

    def _post_put_hook(self, future):
        library_search.update_book(self)

    @classmethod
    def _post_delete_hook(cls, key, future):
        library_search.delete_book(key.id())


class LibraryUser(ndb.Model):
    id = ndb.StringProperty()
    email = ndb.StringProperty()
    name = ndb.StringProperty(default='default')
    type = ndb.StringProperty(default='new')