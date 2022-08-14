from django.urls import path
from . import views

urlpatterns = [
    path('iframe/<str:room_name>/', views.iframe_chat_room_view, name='iframe-chat-room'),
    path('<str:room_name>/', views.chat_room_view, name='chat-room'),
]
