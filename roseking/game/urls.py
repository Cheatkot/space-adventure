from django.urls import path
from . import views

urlpatterns = [
    path('demo/', views.game_demo, name='game_demo'),
]
