import django.core.handlers.wsgi
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django.settings")
application = django.core.handlers.wsgi.WSGIHandler()