from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from mongoengine.django.auth import User as MongoUser
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login
import requests
import uuid
import cookielib
import urllib2
import Cookie
from user_profile.models import User

# Create your views here.

def index(request):
    try:
        user_id = request.session['user_id']
        template = loader.get_template('login/already-logged-in.html')
        user1 = User.objects.get(id=user_id)
        return HttpResponse(template.render({'username':user1.username}, request))
    except KeyError:
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
        template = loader.get_template('login/index.html')
        try:
            user1 = User.objects.get(username=username)
            if user1.check_password(password):
                request.session['user_id'] = str(user1.id)
                request.session.set_expiry(3600)
                print user1.id
                return HttpResponseRedirect('/')
            else:
                return HttpResponse(template.render({'alert': 'Wrong Password', 'username': username}, request))
        except:
            return HttpResponse(template.render({'alert': 'User not found', 'username': username}, request))
            #return HttpResponse("This user does not exists. Please try again.")
    return HttpResponse("No Response")

