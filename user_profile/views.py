from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine.django.auth import User
from . import models
from django.template import loader

# Create your views here.

def index(request):
    try:
        user1 = User.objects.get(id=request.session['user_id'])
        request.session.set_expiry(3600)
        print user1.username
        template = loader.get_template('user_profile/index.html')
        pass_data = {'username': user1.username,
            'email': user1.email}
        if user1.email == None:
            pass_data['email'] = " "
        return HttpResponse(template.render(pass_data, request))
        #return HttpResponse("AAA")
    except:
        template = loader.get_template('notlogin.html')
        return HttpResponse(template.render({}, request))
