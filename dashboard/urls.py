from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('loginform/', views.user_login, name='login'),
]