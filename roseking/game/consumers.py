from datetime import datetime
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .helper import Game, active_games
# from .models import XXX


class MainGameConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.game_id = None
        self.game = None
        self.user = None
        self.player_number = None

    def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.user = self.scope['user']

        if self.game_id not in active_games.keys():
            active_games[self.game_id] = Game(self.game_id, self.user)
            self.player_number = 1

        self.game = active_games[self.game_id]

        if self.game.add_player_two(self.user) != -1:
            self.player_number = 2
        else:
            return

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.game_id,
            self.channel_name,
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.game_id,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        game_message_type = text_data_json['type']
        message = text_data_json['message']

        if not self.user.is_authenticated:
            return

        if game_message_type == "draw_card":
            async_to_sync(self.channel_layer.group_send)(
                self.game_id,
                {
                    'type': 'draw_card',
                    'username': self.user.username,
                    'target_position': message["target_position"],
                    'player_number': self.player_number,
                    'points': message["points"],
                }
            )
        elif game_message_type == "play_card":
            if self.game.check_move_possibility(self.player_number, message['card_id']) == 0:
                async_to_sync(self.channel_layer.group_send)(
                    self.game_id,
                    {
                        'type': 'play_card',
                        'username': self.user.username,
                        'target_position': self.game.calc_beer_mug_position(self.player_number, message['card_id']),
                        'player_number': self.player_number,
                        'played_card': self.game.play_card(self.player_number, message['card_id'], False),
                        'points': self.game.calc_player_points(),
                    }
                )
            else:
                async_to_sync(self.channel_layer.group_send)(
                    self.game_id,
                    {
                        'type': 'game_error',
                        'message': 'Diese Karte kann nicht gespielt werden!',
                    }
                )
        elif game_message_type == "play_joker_card":
            if self.game.check_move_possibility(self.player_number, message['card_id']) == 1:
                async_to_sync(self.channel_layer.group_send)(
                    self.game_id,
                    {
                        'type': 'play_card',
                        'username': self.user.username,
                        'target_position': self.game.calc_beer_mug_position(self.player_number, message['card_id']),
                        'player_number': self.player_number,
                        'played_card': self.game.play_card(self.player_number, message['card_id'], True),
                        'points': self.game.calc_player_points(),
                    }
                )
            else:
                async_to_sync(self.channel_layer.group_send)(
                    self.game_id,
                    {
                        'type': 'game_error',
                        'message': 'Diese Karte kann nicht gespielt werden!',
                    }
                )
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.game_id,
                {
                    'type': 'game_error',
                    'message': 'Unbekannte Aktion!',
                }
            )

    def draw_card(self, event):
        self.send(text_data=json.dumps(event))

    def play_card(self, event):
        self.send(text_data=json.dumps(event))

    def play_joker_card(self, event):
        self.send(text_data=json.dumps(event))

    def game_error(self, event):
        self.send(text_data=json.dumps(event))
