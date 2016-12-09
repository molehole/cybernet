"""projekt URL Configuration

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
from django.conf.urls import url, include
from terminal import views

urlpatterns = [
    url(r'^szwalnia/status/$', views.szwalnia, name='szwalnia'),
    url(r'^szwalnia/przekaz/$', views.szwalnia_przekaz, name='szwalnia_przekaz'),
    url(r'^stolarnia/status/$', views.stolarnia name='stolarnia),
    url(r'^stolarnia/przekaz/$', views.stolarnia_przekaz, name='stolarnia_przekaz'),
    url(r'^bufor/status/$', views.bufor, name='bufor'),
    url(r'^bufor/przekaz/$', views.bufor_przekaz, name='bufor_przekaz'),
    url(r'^bufor/oddaj/$', views.bufor_oddaj, name='bufor_oddaj'),
    url(r'^bufor/potwierdz/$', views.bufor_potwierdz, name='bufor_potwierdz'),
    url(r'^bufor/przekaz/$', views.bufor_sprawdz, name='bufor_sprawdz'),
    url(r'^testowa/$', views.Testowa, name='strona_testowa_index'),
]
