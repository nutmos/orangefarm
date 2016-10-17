from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

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
    return HttpResponse(template.render({'foo':'bar'}, request))
