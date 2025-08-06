from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.registeration, name='register'),
    path('about-us', views.aboutUs, name='about-us'),
    path('courses', views.courses, name='courses'),
    path('contact-us', views.aboutUs, name='contact-us'),
]
