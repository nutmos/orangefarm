from django.shortcuts import render
from login.models import *
from django.http import HttpResponse
from django.template import loader
from mongoengine.django.auth import User

# Create your views here.

def index(request):
    template = loader.get_template('login/index.html')
    #a = User.objects.create(
    #    username="Nutmos", password="111")
    #a.save()
    return HttpResponse(template.render({'foo': 'bar'}, request))
    #return HttpResponse("<h1>Success!</h1>")

def login_status(request):
    if request.method == "POST":
        username = request.POST.get("username","")
        password = request.POST.get("password", "")
        user1 = User.objects.get(username=username)
        if user1.check_password(password):
            #user1.backend = 'mongoengine.django.auth.MongoEngineBackend'
            #request.session.set_expiry(60*60*1)
            #request.session["username"] = username
            #print request.session
            #template = loader.get_template('index.html')
            #return HttpResponse(template.render({'foo':'bar'}, request))
            return HttpResponse("True")
        else:
            return HttpResponse("False")
    return HttpResponse("No Response")
