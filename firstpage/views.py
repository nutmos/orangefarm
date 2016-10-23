from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

is_login = True

def get_is_login():
    return is_login

# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    #a = User.objects.create(
    #    username="Nutmos", password="111")
    #a.save()
    #if (request.session['username'] == 'nutmos'):
    #    return HttpResponse("True")
    #else:
    #    return HttpResponse(template.render({'foo': 'bar'}, request))
    #return HttpResponse("<h1>Success!</h1>")
    is_login = True
    try:
        a = request.session['user_id']
        print 'user_id = ' + a
    except KeyError:
        print "KeyError"
        is_login = False
    print 'is_login = ' + str(is_login)
    return HttpResponse(template.render({'foo':'bar'}, request))
