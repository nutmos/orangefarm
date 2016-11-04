from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine import *
from models import *
from django.template import loader


# Create your views here.

def index(request):
    template = loader.get_template('country/index.html')
    return HttpResponse(template.render({'foo': 'bar'}, request))

def add_country(request):
    if request.method == 'GET':
        name = request.GET.get('name','')
        if name != None:
            description = request.GET.get('description', '')
            print name
            print description
            c1 = Country(name=name, description=description)
            c1.save()
            return HttpResponseRedirect('/')
    template = loader.get_template('country/edit.html')
    return HttpResponse(template.render({}, request))

def index(request):
    if request.method == 'GET':
        country_id = request.GET.get('country-id', '')
        c1 = Country.objects.get(id=country_id)
        template = loader.get_template('country/index.html')
        pass_data = {
            'name': c1.name, 
            'description': c1.description,
            'country_id': country_id}
        return HttpResponse(template.render(pass_data, request))
    return HttpResponse('This page is not complete')

def edit(request):
    if request.method == 'GET':
        country_id = request.GET.get('country-id', '')
        print country_id
        try:
            c1 = Country.objects.get(id=country_id)
            template = loader.get_template('country/edit.html')
            pass_data = {
                'name': c1.name,
                'description': c1.description,
                'country_id': country_id}
            return HttpResponse(template.render(pass_data, request))
        except:
            return HttpResponse('Key error')
    return HttpResponse('No request')

def process_edit(request):
    if request.method == 'GET':
        desc = request.GET.get('description', '')
        country_id = request.GET.get('country-id', '')
        c1 = Country.objects.get(id=country_id)
        c1.description = request.GET.get('description', '')
        c1.save()
        template = loader.get_template('country/process-edit.html')
        pass_data = {'country_id': country_id};
        return HttpResponse(template.render(pass_data, request))
    return HttpResponse('No Request')
