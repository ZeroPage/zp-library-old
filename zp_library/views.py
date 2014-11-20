from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import *
from django.utils import timezone
from zp_library.models import Book
from zp_library.forms import *


import urllib
import urllib2
import json


class MainPageView(TemplateView):
	template_name = 'zp_library/main_page.html'

	def get_context_data(self, **kwargs):
		context = super(MainPageView, self).get_context_data(**kwargs)
		context['message'] = 'test'

		return context

class TestView(FormView):
	template_name = 'zp_library/form.html'
	form_class = BookForm
	success_url = '/'


	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		form.action()
		return super(TestView, self).form_valid(form)


class ParseView(TemplateView):
	template_name = 'zp_library/parse.html'

	def get_context_data(self, **kwargs):
		context = super(ParseView, self).get_context_data(**kwargs)

		isbn = '9788966260546'
		#isbn = request.GET.get('isbn', '9788966260546')
		json_result = json.load(urllib2.urlopen('https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn))

		context['result'] = json.dumps(json_result, indent = 4, ensure_ascii = False, separators = (',', ': '))

		return context