from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name = 'log_in'),
    path('singUp', views.singUp, name = 'singup'),
]