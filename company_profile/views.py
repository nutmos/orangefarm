from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from models import *

# Create your views here.

def index(request):
    if request.method == 'GET':
        com_id = request.GET.get('company_id', '')
        com1 = Company.objects.get(id=com_id)
        template = loader.get_template('company_profile/index.html')
        return HttpResponse(template.render({
            'name': com1.name,
            'description': com1.description,
            'location': com1.location,
            'company_id': com1.id
            }, request))
    return HttpResponse('The page does not complete')

def edit(request):
    if request.method == 'GET':
        com_id = request.GET.get('company_id', '')
        com1 = Company.objects.get(id=com_id)
        template = loader.get_template('company_profile/edit.html')
        pass_data = {
            'name': com1.name,
            'description': com1.description,
            'location': com1.location,
            'company_id': com_id,
        }
        return HttpResponse(template.render(pass_data, request))
    return HttpResponse('The page is not complete')

def process_edit(request):
    if request.method == 'GET':
        com_id = request.GET.get('company_id', '')
        com1 = Company.objects.get(id=com_id)
        com1.name = request.GET.get('name', '')
        com1.description = request.GET.get('description', '')
        com1.location = request.GET.get('location', '')
        com1.save()
        return HttpResponseRedirect('/company?company_id=' + str(com_id))
    return HttpResponse('The page is not complete')
