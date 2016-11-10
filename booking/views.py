from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine import *
from models import *
from django.template import loader


# Create your views here.

def index(request):
    template = loader.get_template('booking/index.html')
    return HttpResponse(template.render({'foo': 'bar'}, request))

def step2(request):
    template = loader.get_template('booking/step2.html')
    return HttpResponse(template.render({'foo': 'bar'}, request))

def step3(request):
    template = loader.get_template('booking/step3.html')
    return HttpResponse(template.render({'foo': 'bar'}, request))
