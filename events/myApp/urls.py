"""events URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('api/users', views.users),
    path('api/login', views.login),
    path('api/register', views.register),
    path('api/events', views.allEvents),
    path('api/joinedevents/<str:email>/', views.joinedEvents),
    path('api/createdevents/<str:email>/', views.createdEvents),
    path('api/addevent', views.addEvent),
    path('api/editevent', views.editEvent),
    path('api/joinevent', views.joinEvent),
    path('api/exitevent', views.exitEvent),

]
