from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^process-index/', views.process_index, name='process-index'),
    url(r'^info', views.info, name='info'),
    url(r'^checking/', views.checking, name='checking'),
    url(r'^payment/', views.payment, name='payment'),
]
