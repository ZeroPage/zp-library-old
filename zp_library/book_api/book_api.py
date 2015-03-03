# -*- coding: utf-8 -*-
import urllib
import json
import unittest

def recursive_dict_search(dict_item, keys, found_item):
    for key, value in dict_item.iteritems():
        if key in keys:
            found_item[key] = value
            keys.remove(key)
        elif type(dict_item[key]) is dict:
            recursive_dict_search(dict_item[key], keys, found_item)


def query_filter(result_items, keys):
    result_item = {}
    for item in result_items:
        for key, value in item.iteritems():
            if key in keys:
                result_item[key] = value
                keys.remove(key)
            elif type(item[key]) is dict:
                recursive_dict_search(item[key], keys, result_item)
    return result_item


class Book:
    parameter = ()
    url = ''
    response = {}
    result = {}
    api_key = ''

    def filter(self):
        pass

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

    def request(self, qurey_parameters):
        try:
            self.response = json.load(
                urllib.urlopen(
                    self.url + 
                    "&".join([key + ":" + value for key, value in qurey_parameters.iteritems()])
                )
            )
        except urllib2.HTTPError, e:
            self.response = e.fp.read()


class Daum(Book):
    parameter = ("translator", "pub_nm", "category")

    def __init__(self):
        self.api_key = "19d3273451bd445399b4cc34a4fdbd45a11e5cee"
        self.parameters = ("translator", "pub_nm", "category")
        self.url = "http://apis.daum.net/search/book?apikey=" + self.api_key +  "&output=json&q="

    # def request(self):
    #     self.response_result = json.load(
    #         urllib.urlopen(
    #             "http://apis.daum.net/search/book?q=%s&apikey=19d3273451bd445399b4cc34a4fdbd45a11e5cee&output=json"
    #             % "&".join([key + ":" + value for key, value in query_params.iteritems()])
    #         )
    #     )

    def filter(self):
        self.result = query_filter(self.response_result["items"], list(self.parameter))


class Google(Book):
    def __init__(self):
        self.api_key = "AIzaSyCEFHrF-qRjKkh3p9hvOpY9lhzdOtsS0UE"
        self.url = "https://www.googleapis.com/books/v1/volumes?key=" + self.api_key + "&q="
        self.parameters = ("industryIdentifiers", "authors", "title", "publishedDate", "description", "pageCount", "imageLinks", "language")
        
    def filter(self):
        self.result = query_filter(self.response["items"], list(self.parameters))


class TestBookAPI(unittest.TestCase):
    def setUp(self):
        self.query_params = {
            "isbn": "9788979149883"
        }

    def test_google_response(self):
        google_api = Google()
        google_api.request(self.query_params)
        self.assertIsNotNone(google_api.response)

    def test_daum_response(self):
        daum_api = Daum()
        daum_api.request(self.query_params)
        self.assertIsNotNone(daum_api.response)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBookAPI)
    unittest.TextTestRunner(verbosity=2).run(suite)