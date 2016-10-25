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
    return HttpResponse(template.render({}, request))

def complete_register(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        email = request.POST.get('email', '')
        template = loader.get_template('register/index.html')
        try:
            User.objects.get(username=username)
            pass_data = {
                'alert': 'Username was already taken',
                'username': username,
                'email': email
            }
            return HttpResponse(template.render(pass_data, request))
        except DoesNotExist:
            if password == '':
                return HttpResponse('Please enter password')
            else:
                try:
                    user1 = User(username=username, email=email)
                    user1.set_password(password)
                    print user1.password
                    user1.save()
                    template = loader.get_template('register/create-complete.html')
                    return HttpResponse(template.render({}, request))
                except ValidationError:
                    pass_data = {
                        'alert': 'Your email address is invalid',
                        'email': email,
                        'username': username
                    }
                    return HttpResponse(template.render(pass_data, request))
    return HttpResponse("No Request")
