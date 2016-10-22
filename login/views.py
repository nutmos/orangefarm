from django.shortcuts import render
from login.models import *
from django.http import HttpResponse
from django.template import loader
from mongoengine.django.auth import User
from django.contrib.sessions.models import Session
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
            #request.session['user_id'] = user1.id
            #print user1.id
            #s = requests.session()
            #s.auth = (username, password)
            #session_id = uuid.uuid5(uuid.NAMESPACE_DNS, username)
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

def get_cookie(request):
    expiration = datetime.datetime.now() + datetime.timedelta(days=60)
    cookie = Cookie.SimpleCookie()
    cookie["session"] = uuid.uuid5(uuid.NAMESPACE_DNS, username)
    cookie["session"]["domain"] = ".128.199.215.223:8000"
    cookie["session"]["path"] = "/"
    cookie["session"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")

