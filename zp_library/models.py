from google.appengine.ext import ndb

DEFAULT_BOOK_NAME = 'default_book'

def book_key(book_name=DEFAULT_BOOK_NAME):
    return ndb.Key('Book', book_name)

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
