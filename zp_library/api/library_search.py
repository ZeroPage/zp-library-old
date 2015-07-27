from google.appengine.api import search
from textblob import TextBlob

import string
import re

INDEX_NAME = 'book'


def update_book(book):
    blob = TextBlob(book.description)

    if blob.detect_language() == 'en':
        description = ''
        nouns = filter(lambda x: x[1] == 'NN' or x[1] == 'NNP', blob.tags)

        for noun, tag in nouns:
            description += noun + " "
            description += TextBlob(noun).translate(to='ko').string + " "

    else:
        description = book.description

    book_document = search.Document(
        doc_id=book.ISBN,
        fields=[
            search.TextField(name='title', value=remove_punc(book.title)),
            search.TextField(name='author', value=remove_punc(book.author)),
            search.TextField(name='description', value=remove_punc(description))
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