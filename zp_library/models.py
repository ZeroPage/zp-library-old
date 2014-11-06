from google.appengine.ext import ndb

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
    smallThumbnail = ndb.LinkProperty()
    thumbnail = ndb.LinkProperty()
    pageCount = ndb.IntegerProperty()
    bookCount = ndb.IntegerProperty()
    donor = ndb.StringProperty()
    registrationDate = ndb.DateProperty(auto_now_add=True)