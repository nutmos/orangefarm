from django.shortcuts import render
from login.models import *
from django.http import HttpResponse
from django.template import loader
from mongoengine.django.auth import User
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login
import requests
import uuid
import cookielib
import urllib2
import Cookie

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
            request.session['user_id'] = str(user1.id)
            print user1.id
            #login(request, user1)
            #s = requests.session()
            #s.auth = (username, password)
            #session_id = uuid.uuid5(uuid.NAMESPACE_DNS, username)
            #user1.backend = 'mongoengine.django.auth.MongoEngineBackend'
            #request.session.set_expiry(60*60*1)
            #request.session["username"] = username
            #print request.session
            #template = loader.get_template('index.html')
            #return HttpResponse(template.render({'foo':'bar'}, request))
            return HttpResponse('True<a href="/login/logout/">Logout</a>')
        else:
            return HttpResponse("False")
    return HttpResponse("No Response")

def logout(request):
    print request.session['user_id']
    try:
        del request.session['user_id']
    except KeyError:
        return HttpResponse('You are not logged in')
    return HttpResponse('Logout')
