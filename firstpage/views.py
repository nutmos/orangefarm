from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from country.models import *

is_login = True

def get_is_login():
    return is_login

# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    is_login = True
    try:
        a = request.session['user_id']
        request.session.set_expiry(3600)
    except KeyError:
        is_login = False
    all_country = Country.objects()
    show_more_country = False
    if len(all_country) > 6:
        import random
        num_list = random.sample(range(len(all_country)), 6)
        print num_list
        all_country = [all_country[num_list[i]] for i in range(6)]
        show_more_country = True
    pass_data = {
        'all_country': all_country,
        'show_more_country': show_more_country
    }
    return HttpResponse(template.render(pass_data, request))

