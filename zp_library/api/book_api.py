# -*- coding: utf-8 -*-
"""
This module is for Book api.
"""
import urllib2
import json
from zp_library.api import isbn as ISBN
import unittest


def recursive_dictionary_search(dict_item, keys, found_item):
    for key, value in dict_item.iteritems():
        if key in keys:
            found_item[key] = value
        elif type(dict_item[key]) is dict:
            recursive_dictionary_search(dict_item[key], keys, found_item)


def response_filter(result_items, keys):
    result_item = {}
    item = result_items[0]

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
        self.parameters = (
            "author_t", "sale_price", "cover_s_url",
            "pub_date", "etc_author", "author", "title",
            "category", "translator", "pub_nm",
            "isbn", "cover_l_url", "description"
        )

    def filter(self):
        if self.response is None:
            self.result = None
            return None
        self.result = response_filter(self.response["channel"]["item"], self.parameters)

        self.result["isbn"] = ISBN.convertISBN(self.result["isbn"])
        if len(self.result["pub_date"]) == 8:
            self.result["pub_date"] = \
                self.result["pub_date"][:4] + \
                "-" + self.result["pub_date"][4:6] + \
                "-" + self.result["pub_date"][6:]

    def request(self, request_parameters):
        try:
            self.response = json.load(
                urllib2.urlopen(
                    self.url +
                    request_parameters["isbn"] + "&searchType=isbn"
                )
            )
            if self.response["channel"]["result"] == "0":
                self.response = None
        except urllib2.HTTPError, e:
            self.response = e.fp.read()


class Google():
    # Google thumbnail size use zoom option, it means thumbnail size is eqaul.
    def __init__(self):
        self._api_key = "AIzaSyCEFHrF-qRjKkh3p9hvOpY9lhzdOtsS0UE"
        self.url = "https://www.googleapis.com/books/v1/volumes?country=KR&key=" + self._api_key + "&q="
        self.parameters = (
            "title", "authors", "publisher",
            "publishedDate", "industryIdentifiers", "pageCount",
            "imageLinks", "language", "description"
        )

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

        try:
            smallThumbnail = self.result["imageLinks"]["smallThumbnail"]
            thumbnail = self.result["imageLinks"]["thumbnail"]
            del self.result["imageLinks"]
            self.result["smallThumbnail"] = smallThumbnail
            self.result["thumbnail"] = thumbnail

            if len(self.result["publishedDate"]) <= 4:
                self.result["publishedDate"] += "-01-01"
            elif len(self.result["publishedDate"]) <= 6:
                self.result["publishedDate"] += "-01"
            elif len(self.result["publishedDate"]) <= 8:
                self.result["publishedDate"] = \
                    self.result["publishedDate"][:4] + \
                    "-" + self.result["publishedDate"][4:6] + \
                    "-" + self.result["publishedDate"][6:]
        except KeyError:
            pass

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


            # raise e


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
        "smallThumbnail" : ["smallThumbnail", "cover_s_url"],
        "thumbnail" : ["thumbnail", "cover_l_url"],
        "pageCount" : ["pageCount", None],
        "description" : "description",
    }

    for key, value in select_rule.iteritems():
        if not google_data and not daum_data:
            break

        try:
            if daum_data:
                if isinstance(value, str):
                    book_data[key] = daum_data[value]
                elif value[1]:
                    book_data[key] = daum_data[value[1]]

            if google_data:
                if isinstance(value, str):
                    book_data[key] = google_data[value]
                elif value[0]:
                    book_data[key] = google_data[value[0]]
        except KeyError:
            pass

    return book_data
