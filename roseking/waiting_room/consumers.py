import json
from channels.generic.websocket import WebsocketConsumer
from random import randint
from time import sleep

class WaitingRoom(WebsocketConsumer):
    def connect(self):
        self.accept()
        for i in range(1000):
            self.send(json.dumps({'user': randint(1, 100)}))
            sleep(1)

    def disconnect(self, code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['user']

        self.send(text_data=json.dumps({
            'message': message
        }))