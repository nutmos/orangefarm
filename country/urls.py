from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^all/', views.all_country, name='all-country'),
    url(r'^add/',views.add_country, name='add-country'),
    url(r'^edit/', views.edit, name='edit'),
    url(r'^process-add/', views.process_add, name='process-add'),
    url(r'^process-edit/', views.process_edit, name='process-edit'),
    url(r'^delete/', views.delete, name='delete'),
    url(r'^handle-change-picture/', views.handle_change_picture, name='handle-change-picture'),
    url(r'^picture/', views.show_image, name='picture'),
    url(r'^c/(?P<country_name>\w+)/', include([
        url(r'^$', views.country_name, name='user'),
        url(r'^city/', views.show_city, name='show-city'),
        url(r'^popular-place/', views.popular_place, name='popular-place'),
        ]))
]
