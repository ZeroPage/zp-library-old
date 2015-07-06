from google.appengine.ext import ndb
from zp_library.models import ExtraVariable

DAUM_BOOK_API_KEY = 'daum_book_api'
GOOGLE_BOOK_API_KEY = 'google_book_api'

key_list = [
    DAUM_BOOK_API_KEY,
    GOOGLE_BOOK_API_KEY,
]

class ExtraVariableKeyError(Exception):
    pass

def get_extra_variable(key):
    result = ndb.Key(ExtraVariable, key).get()

    if result is None:
        raise ExtraVariableKeyError(key)

    return result.value

def set_extra_variable(key, value):
    ExtraVariable(key=ndb.Key(ExtraVariable, key), value=value).put()
