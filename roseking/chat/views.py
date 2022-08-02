from django.shortcuts import render
from .models import ChatRoom


def chat_room_view(request, room_name):
    chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
    return render(request, 'chat/chat-room.html', {
        'chat_room': chat_room,
    })
