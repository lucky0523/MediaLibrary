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
from django.views.static import serve
from django.conf import settings

from MediaLibrary import views
from WebPage import views as WebPage_views

urlpatterns = [
    re_path(r'^$', WebPage_views.nav),
    path('upload/', views.receive),
    path('match/', views.match),
    path('image', views.refresh_images),
    path('test', views.test_local),
    path('test_return', views.test_return),
    path('nav/', WebPage_views.nav),
    path('imgs', WebPage_views.gallery),
    path('gallery', WebPage_views.gallery),
    re_path('dynamic/(?P<path>.*)', serve, {'document_root': settings.DYNAMIC_ROOT}),
]
