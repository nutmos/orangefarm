from django.shortcuts import render
from login.models import *
from django.http import HttpResponse, HttpResponseRedirect
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

def logout(request):
    #print request.session['user_id']
    try:
        del request.session['user_id']
    except KeyError:
        return HttpResponse('You are not logged in')
    template = loader.get_template('logout/index.html')
    return HttpResponse(template.render({'foo': 'bar'}, request))
