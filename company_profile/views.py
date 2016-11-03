from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from models import *

# Create your views here.

def index(request):
    if request.method == 'GET':
        com_id = request.GET.get('company_id', '')
        com1 = Company.objects.get(id=com_id)
        print com_id
        template = loader.get_template('company_profile/index.html')
        return HttpResponse(template.render({
            'name': com1.name,
            'description': com1.description,
            'location': com1.location
            }, request))
    return HttpResponse('The page does not complete')
