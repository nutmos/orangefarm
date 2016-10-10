from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^showdata/', views.showdata, name='showdata'),
    url(r'^select/', views.select, name='select'),
    url(r'^update/', views.update, name='update'),
    url(r'^doUpdate/', views.doUpdate, name='doUpdate'),
    url(r'^delete/', views.delete, name='delete'),
]
