# -*- coding: utf-8 -*-
"""
This module is for Book api.
"""
import urllib
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


class Book:
    def pretty(self, type_):
        if type_ == "response":
            obj = self.response
        elif type_ == "result":
            obj = self.result

        return json.dumps(
                obj,
                indent = 4,
                separators = (",", ": ")
            )

    def request(self, request_parameters):
        try:
            self.response = json.load(
                urllib.urlopen(
                    self.url + 
                    "&".join([key + ":" + value for key, value in request_parameters.iteritems()])
                )
            )
        except urllib2.HTTPError, e:
            self.response = e.fp.read()


class Daum(Book):
    """

    
    """
    def __init__(self):
        self._api_key = "19d3273451bd445399b4cc34a4fdbd45a11e5cee"
        self.url = "http://apis.daum.net/search/book?apikey=" + self._api_key +  "&output=json&q="
        self.parameters = ("author_t", "sale_price", "cover_s_url", "pub_date", "etc_author", "author", "title", "category", "translator", "pub_nm", "isbn13", "cover_l_url")
        # ("translator", "pub_nm", "category")

    def filter(self):
        self.result = response_filter(self.response["channel"]["item"], self.parameters)


class Google(Book):
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
    def __init__(self):
        self._api_key = "AIzaSyCEFHrF-qRjKkh3p9hvOpY9lhzdOtsS0UE"
        self.url = "https://www.googleapis.com/books/v1/volumes?key=" + self._api_key + "&q="
        self.parameters = ("industryIdentifiers", "authors", "title", "publishedDate", "description", "pageCount", "imageLinks", "language")
        
    def filter(self):
        self.result = response_filter(self.response["items"], self.parameters)

        isbn = self.result["industryIdentifiers"][0]["identifier"]
        if len(isbn) == 10:
            self.result["isbn"] = ISBN.convertISBN(isbn)
        else:
            self.result["isbn"] = isbn

        del self.result["industryIdentifiers"]


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