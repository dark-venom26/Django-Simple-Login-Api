from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('allusers', views.allUsers, name='allUsers'),
    path('register', views.registerUser, name='registerUser'),
    path('login', views.loginUser, name='loginUser'),
]


