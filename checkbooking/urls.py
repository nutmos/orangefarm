from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^process_confirm', views.process_confirm, name='process_confirm')
]
