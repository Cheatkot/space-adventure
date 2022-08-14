from django.shortcuts import render
from .models import ChatRoom
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required


@login_required
def chat_room_view(request, room_name):
    chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
    return render(request, 'chat/chat-room.html', {
        'chat_room': chat_room,
    })


@login_required
@xframe_options_exempt
def iframe_chat_room_view(request, room_name):
    chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
    return render(request, 'chat/iframe-chat-room.html', {
        'chat_room': chat_room,
    })
