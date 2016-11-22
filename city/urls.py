from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/',views.add_city, name='add-city'),
    url(r'^edit/', views.edit, name='edit'),
    url(r'^process-add/', views.process_add, name='process-add'),
    url(r'^process-edit/', views.process_edit, name='process-edit'),
    url(r'^delete/', views.delete, name='delete'),
    url(r'^picture/', views.show_image, name='image'),
    url(r'^handle-change-picture/', views.handle_change_picture, name='handle-change-picture'),
    url(r'^get-city-by-country/',views.get_city_by_country, name='get-city-by-country'),
    url(r'^c/(?P<city_name>\w+)/', include ([
        url(r'^$', views.city_name, name='city_name'),
        url(r'^popular-place/', views.popular_place, name='popular-place'),
    ]))
]
