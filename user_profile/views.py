from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine.django.auth import User as MongoUser
from user_profile.models import *
from django.template import loader

# Create your views here.

def index(request):
    try:
        user1 = User.objects.get(id=request.session['user_id'])
        request.session.set_expiry(3600)
        print user1.photo
        template = loader.get_template('user_profile/index.html')
        pass_data = {'username': user1.username,
            'email': user1.email,
            'bio': user1.bio,
            'name': user1.name}
        if user1.email == None:
            pass_data['email'] = ''
        return HttpResponse(template.render(pass_data, request))
        #return HttpResponse("AAA")
    except:
        template = loader.get_template('notlogin.html')
        return HttpResponse(template.render({}, request))

def show_image(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id', '')
        print user_id
        user1 = User.objects.get(id=user_id)
        binary_img = user1.photo.read()
        return HttpResponse(binary_img, 'image/png')
    return HttpResponse('This page not complete')

def edit_profile(request):
    if request.method == 'POST':
        user1 = User.objects.get(id=request.session['user_id'])
        user1.email = request.POST.get('email', '')
        user1.bio = request.POST.get('bio', '')
        user1.name = request.POST.get('name', '')
        print user1.name
        print user1.bio
        print user1.email
        user1.save()
        return HttpResponseRedirect('/profile/')
    else:
        try:
            print request.session['user_id']
            user1 = User.objects.get(id=request.session['user_id'])
            request.session.set_expiry(3600)
            template = loader.get_template('user_profile/edit.html')
            pass_data = {'username': user1.username,
                'email': user1.email,
                'bio': user1.bio,
                'name': user1.name}
            print "Bio = " + user1.bio
            if user1.email == None:
                pass_data['email'] = ""
            if user1.bio == None:
                pass_data['bio'] = ""
            if user1.name == None:
                pass_data['name'] = ""
            return HttpResponse(template.render(pass_data, request))
        except DoesNotExist:
            template = loader.get_template('notlogin.html')
            return HttpResponse(template.render({}, request))

def change_password(request):
    if request.method == 'POST':
        try:
            user1 = User.objects.get(id=request.session['user_id'])
            password1 = request.POST.get('current-password', '')
            password2 = request.POST.get('new-password', '')
            password3 = request.POST.get('verify-password', '')
            if password2 == password3:
                if user1.check_password(password1):
                    user1.set_password(password2)
                    template = loader.get_template('user_profile/index.html')
                    return HttpResponse('Your password was successfully changed.')
                else:
                    return HttpResponse('The current password was not correct')
            else:
                print password2
                print password3
                return HttpResponse('New password and verify password does not match')
        except DoesNotExist:
            template = loader.get_template('notlogin.html')
            return HttpResponse(template.render({}, request))
    else:
        try:
            user1 = User.objects.get(id=request.session['user_id'])
            template = loader.get_template('user_profile/change-password.html')
            return HttpResponse(template.render({}, request))
        except DoesNotExist:
            template = loader.get_template('notlogin.html')
            return HttpResponse(template.render({}, request))
