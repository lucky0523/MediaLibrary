"""MediaLibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from MediaLibrary import views, testdb
from WebPage import views as WebPage_views

urlpatterns = [
    re_path(r'^$', views.hello),
    path('testdb/', testdb.read_db),
    path('imgs/', WebPage_views.imgs),
    path('upload/', testdb.upload),
    path('match/', testdb.match),
    path('image/', testdb.refresh_images),
]
