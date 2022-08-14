from django.urls import path
from . import views

urlpatterns = [
    path('demo/', views.game_demo, name='game_demo'),
    path('<str:game_id>/', views.main_game, name='main_game'),
]
