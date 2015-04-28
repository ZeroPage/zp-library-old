from zp_library.models import BookBorrow, Book
from datetime import datetime


class NoBorrowException(Exception):
    pass


class MaxBorrowException(Exception):
    pass


# fixme - new book api should have NoBookFoundException
class NoBookFoundException(Exception):
    pass


def get_borrows(isbn=None, user_id=None, only_unreturned=False):
    query = BookBorrow.query()
    query = query.order(-BookBorrow.borrowDate)

    if only_unreturned:
        query = query.filter(BookBorrow.returnDate == None)

    if isbn:
        query = query.filter(BookBorrow.ISBN == isbn)

    if user_id:
        query = query.filter(BookBorrow.userID == user_id)

    return query.fetch()


def book_return(isbn, user_id):
    my_borrow = get_borrows(isbn, user_id, True)

    if not my_borrow:
        raise NoBorrowException

    for borrow_record in my_borrow:
        borrow_record.returnDate = datetime.now()
        borrow_record.put()


def book_borrow(isbn, user_id):
    unreturned_borrow_count = BookBorrow.query(BookBorrow.ISBN == isbn, BookBorrow.returnDate == None).count()
    book_result = Book.query(Book.ISBN == isbn).fetch()[0]

    if not book_result:
        raise NoBookFoundException('No Book')

    if unreturned_borrow_count >= book_result.bookCount:
        raise MaxBorrowException('Max borrow reached')

    new_borrow = BookBorrow()
    new_borrow.ISBN = isbn
    new_borrow.userID = user_id

    new_borrow.put()