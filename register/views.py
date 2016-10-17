from django.shortcuts import render
from login.models import *
from django.http import HttpResponse
from django.template import loader
from mongoengine.django.auth import User
from . import models

def index(request):
    template = loader.get_template('register/index.html')
    #a = User.objects.create(
    #    username="Nutmos", password="111")
    #a.save()
    return HttpResponse(template.render({'foo': 'bar'}, request))

def complete_register(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        email = request.POST.get('email', '')
        try:
            User.objects.get(username=username)
            return HttpResponse("User Exists")
        except DoesNotExist:
            user1 = User(username=username, email=email)
            user1.set_password(password)
            print user1.password
            user1.save()
            return HttpResponse("Create User Completed")
    return HttpResponse("No Request")
