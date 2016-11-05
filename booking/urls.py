from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^step2/', views.step2, name='step2'),
    url(r'^step3/', views.step3, name='step3'),
]
