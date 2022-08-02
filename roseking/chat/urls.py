from django.urls import path
from . import views

urlpatterns = [
    path('<str:room_name>/', views.chat_room_view, name='chat-room'),
]
