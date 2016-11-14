from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine import *
from models import *
from django.template import loader


# Create your views here.

def index(request):
    template = loader.get_template('booking/index.html')
    return HttpResponse(template.render({'foo': 'bar'}, request))

def info(request):
    template = loader.get_template('booking/info.html')
    return HttpResponse(template.render({'foo': 'bar'}, request))

def checking(request):
    template = loader.get_template('booking/checking.html')
    return HttpResponse(template.render({'foo': 'bar'}, request))

def payment(request):
    template = loader.get_template('booking/payment.html')
    return HttpResponse(template.render({'foo': 'bar'}, request))
