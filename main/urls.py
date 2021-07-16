from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.create_user),
    path('user_page', views.user_page),
    path('login', views.login),
    path('logout', views.logout)
]