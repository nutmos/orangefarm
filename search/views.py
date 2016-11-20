from django.shortcuts import render
from login.models import *
from django.http import HttpResponse
from django.template import loader
import urllib
from country.models import *

# Create your views here.

def index(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        query_unquote =  urllib.unquote(query)
        country_list = Country.objects.exec_js("""
                function() {
                    var country = [];
                    db[collection].find(query).forEach(function(doc) {
                        if (doc.name.search('""" + query_unquote + """')) {
                            country.push(doc)
                        }
                    })
                    country.forEach(function(object) {
                        object['id'] = object['_id'];
                        delete object['_id'];
                    })
                    return country;
                    }
                    """
                )
        print country_list[0]["name"]
        print country_list
        pass_data = {
            'query': query_unquote,
            'country_list': country_list,
        }
        template = loader.get_template('search/index.html')
        return HttpResponse(template.render(pass_data, request))
    return HttpResponse("Not Complete")
