from django.http import HttpResponseRedirect
from django.contrib import messages

from zp_library.models import LibraryUser
from google.appengine.api import users

USER_TYPE_ADMIN = 'admin'
USER_TYPE_AUTH = 'auth'
USER_TYPE_NEW = 'new'

class NotGoogleLoggedInError(Exception):
    pass

class AlreadySignedUpError(Exception):
    pass

def get_library_user(user_id=None):
    """
    :param user_id: user's id. if not given, current user's id is used.
    :return: library user's information
    """
    if not user_id:
        google_user = get_google_user()

        if not google_user:
            return None

        user_id = google_user.user_id()

    library_user = LibraryUser.query(LibraryUser.id == user_id).get()

    if not library_user:
        return None

    return library_user


def get_google_user():
    return users.get_current_user()


def get_login_url(dest='/'):
    """
    request proper URL to login.

    :param dest: destination URL after login.
    :return: proper URL to be logged in.
    """
    google_user = users.get_current_user()

    if not google_user:
        return users.create_login_url(dest)

    library_user = get_library_user(google_user.user_id())

    if not library_user:
        return '/signup'

    return dest


def get_logout_url(dest='/'):
    return users.create_logout_url(dest)

def add_user(name):
    google_user = get_google_user()

    if not google_user:
        raise NotGoogleLoggedInError

    library_user = get_library_user(google_user.user_id())

    if library_user:
        raise AlreadySignedUpError

    if users.is_current_user_admin():
        user_type = USER_TYPE_ADMIN
    else:
        user_type = USER_TYPE_NEW

    LibraryUser(id=google_user.user_id(), email=google_user.email(),
                name=name, type=user_type).put()

def not_authorized(request, dest='/'):
    messages.error(request, 'not authorized.')

    return HttpResponseRedirect(dest)
