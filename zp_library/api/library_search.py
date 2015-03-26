from google.appengine.api import search

import string
import re

INDEX_NAME = 'book'


def update_book(book):
    book_document = search.Document(
        doc_id=book.ISBN,
        fields=[
            search.TextField(name='title', value=remove_punc(book.title)),
            search.TextField(name='author', value=remove_punc(book.author)),
            search.TextField(name='description', value=remove_punc(book.description))
        ]
    )

    index = get_book_index()
    index.put(book_document)


def delete_book(isbn):
    index = get_book_index()
    index.delete(isbn)


def search_book(query):
    index = get_book_index()
    query_string = query

    return index.search(query_string)


def get_book_index():
    return search.Index(name=INDEX_NAME)


def remove_punc(target):
    return re.sub('[' + string.punctuation + ']', ' ', target)