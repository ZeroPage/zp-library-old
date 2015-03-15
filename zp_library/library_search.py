from google.appengine.api import search

INDEX_NAME = 'book'


def add_book(isbn, title):
    book_document = search.Document(
        doc_id=isbn,
        fields=[
            search.TextField(name='title', value=title)
        ]
    )

    index = get_book_index()
    index.put(book_document)


def delete_book(isbn):
    index = get_book_index()
    index.delete(isbn)


def search_book_title(title):
    index = get_book_index()
    query_string = "title: " + title

    return index.search(query_string)


def get_book_index():
    return search.Index(name=INDEX_NAME)