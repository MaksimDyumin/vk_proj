"""
URL configuration for django_friends_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from rf_friends_service import views


urlpatterns = [
  path('', views.HelloWorldView.as_view()),
  path('register/', views.RegistrationView.as_view()),

  path('user/friends/', views.HelloWorldView.as_view()), # список друзей (GET)
  path('user/friends/<int:pk>', views.HelloWorldView.as_view()), # пользователь (инфо о реквесте в друзья GET, удалить из друзей DELETE)

  path('user/friend_requests/incoming/', views.HelloWorldView.as_view()), # список входящих заявок (посмотреть GET)
  path('user/friend_requests/incoming/<int:pk>/', views.HelloWorldView.as_view()), # действия с нужной заявкой (принять PUT, отклонить DELETE)

  path('user/friend_requests/outgoing/', views.HelloWorldView.as_view()),# список исходящих заявок (посмотреть GET, создать POST)
  path('user/friend_requests/outgoing/<int:pk>/', views.HelloWorldView.as_view()),# действия с нужной заявкой (отменить DELETE)
]