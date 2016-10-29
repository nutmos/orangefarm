from django.shortcuts import render
from login.models import *
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
    template = loader.get_template('aboutus/index.html')
    #a = User.objects.create(
    #    username="Nutmos", password="111")
    #a.save()
    return HttpResponse(template.render({'foo': 'bar'}, request))
    #return HttpResponse("<h1>Success!</h1>")
