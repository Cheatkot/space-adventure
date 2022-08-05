from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gamerules/', views.gamerules, name='gamerules'),
]
