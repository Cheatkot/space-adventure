import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

ActiveWaitingRooms = {
}


def get_waiting_room(room_name):
    print("get user from room: " + room_name)
    return ActiveWaitingRooms[room_name]


def add_to_waiting_room(room_name, user):
    if not room_name in ActiveWaitingRooms.keys():
        print('create waiting_room: ' + room_name)
        ActiveWaitingRooms[room_name] = []
    print('add user: ' + user + ' to room: ' + room_name)
    ActiveWaitingRooms[room_name] += [user]


def remove_from_waiting_room(room_name, user):
    if room_name in ActiveWaitingRooms.keys():
        print('remove user: ' + user + ' from room: ' + room_name)
        if user in ActiveWaitingRooms[room_name]:
            print('room found -> remove User')
            ActiveWaitingRooms[room_name].remove(user)


class WaitingRoom(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.text_data = None
        self.room_name = None
        self.room_group_name = None
        self.user = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'waiting_room_%s' % self.room_name
        print(self.room_name)
        print(self.room_group_name)
        self.user = self.scope['user']
        add_to_waiting_room(self.room_name, self.user.username)

        async_to_sync(self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name))
        print('connected')
        print(ActiveWaitingRooms[self.room_name])

        async_to_sync(self.accept())

    def receive(self, text_data):
        print('begin receive')
        self.text_data = json.loads(text_data)
        print(self.text_data['user'])
        add_to_waiting_room(self.text_data['user'])

        users = get_waiting_room(self.room_name)

        print(str(users))

        async_to_sync(self.channel_layer.group_send(self.room_group_name, {
            'type': 'user_list',
            'users': str(users)
        }))

    def disconnect(self, close_code):
        remove_from_waiting_room(self.room_name, self.user.username)
        async_to_sync(self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name))

        users = get_waiting_room(self.room_name)
        print(users)

    # async_to_sync(self.channel_layer.group_send(self.self.room_group_name, {
    #   'type': 'user_list',
    #     'users': str(users)
    # }))

    def user_list(self, event):
        users = event['users']

        async_to_sync(self.send(text_data=users))
