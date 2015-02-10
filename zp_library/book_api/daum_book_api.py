#-*- coding: utf-8 -*-
import urllib
import json


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

class daum:
    parameter = ("translator", "pub_nm", "description", "category")
    response_result = {}
    result = {}

    def __init__(self, query_parameters):
        self.response_result = json.load(
            urllib.urlopen(
                "https://www.googleapis.com/books/v1/volumes?q=%s"
                % "&".join([key + ":" + value for key, value in query_params.iteritems()])
            )
        )

    def filter(self):
        self.result = query_filter(self.response_result["items"], list(self.parameter))

    def pretty(self):
        return json.dumps(
            self.result,
            indent=4,
            separators=(',', ': ')
        )
