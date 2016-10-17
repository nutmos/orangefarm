from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^complete-register/', views.complete_register, name='complete_register'),
]
