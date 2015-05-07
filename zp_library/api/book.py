from zp_library.models import Book
from google.appengine.ext import ndb


class NoBookFoundException(Exception):
    pass


def get_books(offset=0, limit=10, isbn_list=None):
    if isbn_list:
        query = Book.query(Book.ISBN.IN(isbn_list)).order(Book.title)
    else:
        query = Book.query().order(Book.title)

    return query.fetch(offset=offset, limit=limit)


def get_book(isbn):
    result = Book.query(Book.key == ndb.Key(Book, isbn)).fetch(limit=1)

    if not result:
        raise NoBookFoundException('No book (isbn: {})'.format(isbn))

    return result[0]


def get_books_count():
    return Book.query().count()