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

if __name__ == "__main__":
    # isbn = "978-89-6626-054-6"
    # isbn = isbn.replace("-","",4)
    # print isbn
    query_params = {
        "isbn": "9788979149883"
    }
    query = []
    for key, value in query_params.iteritems():
        query.append(key + ":" + value)
    print query
    json_result = json.load(
        urllib.urlopen(
            "https://www.googleapis.com/books/v1/volumes?q=%s"
            % "&".join(query)
        ))
    # print json_result
    print json.dumps(json_result, indent=4, separators=(',', ': '))

    print json.dumps(
        query_filter(
            json_result["items"],
            ["industryIdentifiers", "id", "authors", "title", "publishedDate"]
        ),
        indent=4,
        separators=(',', ': ')
    )
