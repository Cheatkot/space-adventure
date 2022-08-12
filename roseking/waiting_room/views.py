from django.shortcuts import render


def room(request, room_name):
    print(room_name)
    return render(request, 'waiting-room.html', {
        'room_name': room_name
    })
