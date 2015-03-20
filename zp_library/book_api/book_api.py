# -*- coding: utf-8 -*-
"""
This module is for Book api.
"""
import urllib2
import json
from zp_library.book_api import isbn as ISBN
import unittest


def recursive_dictionary_search(dict_item, keys, found_item):
    for key, value in dict_item.iteritems():
        if key in keys:
            found_item[key] = value
        elif type(dict_item[key]) is dict:
            recursive_dictionary_search(dict_item[key], keys, found_item)


def response_filter(result_items, keys):
    result_item = {}
    for item in result_items:
        for key, value in item.iteritems():
            if key in keys:
                result_item[key] = value
            elif type(item[key]) is dict:
                recursive_dictionary_search(item[key], keys, result_item)
    return result_item


class Daum():
    def __init__(self):
        self._api_key = "19d3273451bd445399b4cc34a4fdbd45a11e5cee"
        self.url = "http://apis.daum.net/search/book?apikey=" + self._api_key +  "&output=json&q="
        self.parameters = ("author_t", "sale_price", "cover_s_url", "pub_date", "etc_author", "author", "title", "category", "translator", "pub_nm", "isbn", "cover_l_url")
        # ("translator", "pub_nm", "category")

    def filter(self):
        if self.response is None:
            self.result = None
            return None
        self.result = response_filter(self.response["channel"]["item"], self.parameters)

        if len(self.result["isbn"]) == 10:
            self.result["isbn"] = ISBN.convertISBN(self.result["isbn"])
    def request(self, request_parameters):
        try:
            self.response = json.load(
                urllib2.urlopen(
                    self.url + 
                    request_parameters["isbn"] + "&searchType=isbn"
                )
            )
            if self.response["channel"]["result"] == 0:
                self.response = None
        except urllib2.HTTPError, e:
            self.response = e.fp.read()


class Google():
    """
    Request Parameters:
        intitle: Returns results where the text following this keyword is found in the title.
        inauthor: Returns results where the text following this keyword is found in the author.
        inpublisher: Returns results where the text following this keyword is found in the publisher.
        subject: Returns results where the text following this keyword is listed in the category list of the volume.
        isbn: Returns results where the text following this keyword is the ISBN number.
        lccn: Returns results where the text following this keyword is the Library of Congress Control Number.
        oclc: Returns results where the text following this keyword is the Online Computer Library Center number
    """
    # Google thumbnail size use zoom option, it means thumbnail size is eqaul.
    def __init__(self):
        self._api_key = "AIzaSyCEFHrF-qRjKkh3p9hvOpY9lhzdOtsS0UE"
        self.url = "https://www.googleapis.com/books/v1/volumes?country=KR&key=" + self._api_key + "&q="
        self.parameters = ("title", "authors", "publisher", "publishedDate", "industryIdentifiers", "pageCount", "imageLinks", "language")
        
    def filter(self):
        if self.response is None:
            self.result = None
            return None
        self.result = response_filter(self.response["items"], self.parameters)


        isbn = self.result["industryIdentifiers"][0]["identifier"]
        if len(isbn) == 10:
            self.result["isbn"] = ISBN.convertISBN(isbn)
        else:
            self.result["isbn"] = isbn

        del self.result["industryIdentifiers"]

        author = self.result["authors"][0]
        del self.result["authors"]
        self.result["author"] = author

    def request(self, request_parameters):
        try:
            self.response = json.load(
                urllib2.urlopen(
                    self.url +
                    "+".join([key + ":" + value for key, value in request_parameters.iteritems()])
                )
            )
            if self.response["totalItems"] == 0:
                self.response = None
        except urllib2.HTTPError, e:
            self.response = e.fp.read()


def selectBookData(google_data, daum_data):
    book_data = {}
    select_rule = {
        # data key : [google_key, daum_key]
        "ISBN" : "isbn",
        "title" : "title",
        "author" : "author",
        "publisher" : ["publisher", "pub_nm"],
        "publishedDate" : ["publishedDate", "pub_date"],
        "language" : ["language", None],
        # "smallThumnail" : [False, "cover_s_url"],
        # "thumbnail" : ["", "cover_l_url"], 
        "pageCount" : ["pageCount", None],
    }

    for key, value in select_rule.iteritems():
        if google_data is None and daum_data is None:
            return None
        elif google_data is None:
            if type(value) == type(list()) and value[1] is not None:
                book_data[key] = daum_data[value[1]]
            elif type(value) != type(list()):
                book_data[key] = daum_data[value]
        elif daum_data is None:
            if type(value) == type(list()) and value[0] is not None:
                book_data[key] = google_data[value[0]]
            elif type(value) != type(list()):
                book_data[key] = google_data[value]
        else:
            if type(value) == type(list()):
                if value[0] is None:
                    book_data[key] = daum_data[value[1]]
                if value[1] is None:
                    book_data[key] = google_data[value[0]]
            else:
                book_data[key] = google_data[value]

    return book_data


class TestBookAPI(unittest.TestCase):
    def setUp(self):
        self.request_parameters = {
            "isbn": "9788979149883"
        }

    def test_google_response(self):
        google_api = Google()
        google_api.request(self.request_parameters)
        self.assertIsNotNone(google_api.response)

    def test_google_filtering(self):
        google_api = Google()
        google_api.request(self.request_parameters)
        google_api.filter()
        print(google_api.pretty("result"))

    def test_daum_response(self):
        daum_api = Daum()
        daum_api.request(self.request_parameters)
        self.assertIsNotNone(daum_api.response)

    def test_daum_filtering(self):
        daum_api = Daum()
        daum_api.request(self.request_parameters)
        daum_api.filter()
        print(daum_api.pretty("result"))


if __name__ == "__main__":
    import isbn as ISBN

    suite = unittest.TestLoader().loadTestsFromTestCase(TestBookAPI)
    unittest.TextTestRunner(verbosity=4).run(suite)