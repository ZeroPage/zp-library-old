from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template


import urllib
import urllib2
import json

def main_page(request):
    template_values = {

    }
    return direct_to_template(request, 'zp_library/main_page.html', template_values)

def parse_book(request):
	isbn = request.GET.get('isbn', '9788966260546')

	json_result = json.load(urllib2.urlopen('https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn))

	template_values = {
		'result': json.dumps(json_result, indent = 4, ensure_ascii = False, separators = (',', ': '))
    }

	return direct_to_template(request, 'zp_library/parse.html', template_values)