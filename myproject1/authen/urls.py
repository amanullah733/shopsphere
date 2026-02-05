from django.urls import path

from .views import  *

urlpatterns = [
    path('',login_,name='login_'),
    path('register/',register,name='register'),
    path('profile/',profile,name='profile'),
    path('logout_/',logout_,name='logout_'),

    path('rest_pass/',rest_pass,name='rest_pass'),
    path('forget_pass/',forget_pass,name='forget_pass'),
    path('new_password/',new_password,name='new_password'),

    path('updateprofile/',updateprofile,name='updateprofile')
]