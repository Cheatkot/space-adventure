from datetime import datetime
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import ChatRoom, Message


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = ChatRoom.objects.get(name=self.room_name)
        self.user = self.scope['user']

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        message = message.strip()
        message = message.replace("\n", "<br>")

        print("This is good")
        print(self.user)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # TODO: Timezone ändern

        if not self.user.is_authenticated:
            return

        print("This is better")

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'username': self.user.username,
                'message': message,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        Message.objects.create(user=self.user, room=self.room, content=message)

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))