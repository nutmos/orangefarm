"""orangefarm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls import handler400, handler403, handler404, handler500

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^$', include('firstpage.urls')),
    url(r'^login/', include('login.urls')),
    url(r'^register/', include('register.urls')),
    url(r'^career/', include('career.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^trip/', include('trip.urls')),
    url(r'^logout/', include('logout.urls')),
    url(r'^profile/', include('user_profile.urls')),
    url(r'^aboutus/', include('aboutus.urls')),
    url(r'^company/', include('company_profile.urls')),
    url(r'^country/', include('country.urls')),
]

