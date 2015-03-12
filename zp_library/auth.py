from zp_library.models import LibraryUser
from google.appengine.api import users

USER_TYPE_ADMIN = 'admin'
USER_TYPE_AUTH = 'auth'
USER_TYPE_NEW = 'new'


def get_library_user():
    google_user = get_google_user()

    if not google_user:
        return None

    library_user = LibraryUser.query(LibraryUser.id == google_user.user_id()).get()

    if not library_user:
        return None

    return library_user


def get_google_user():
    return users.get_current_user()


def get_login_url(dest='/'):
    google_user = users.get_current_user()

    if not google_user:
        return users.create_login_url(dest)

    library_user = LibraryUser.query(LibraryUser.id == google_user.user_id()).get()

    if not library_user:
        return '/signup'

    return '/'


def get_logout_url(dest='/'):
    return users.create_logout_url(dest)