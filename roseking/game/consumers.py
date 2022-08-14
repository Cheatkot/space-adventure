from datetime import datetime
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .helper import Game, active_games
from .models import BrezelWar


class MainGameConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.game_id = None
        self.game = None
        self.user = None
        self.player_number = None
        self.finished = False

    def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.user = self.scope['user']
        zwErg_start = False

        if self.game_id not in active_games.keys():
            active_games[self.game_id] = Game(self.game_id, self.user.username)
            self.player_number = 1

        self.game = active_games[self.game_id]

        if self.game.add_player_two(self.user.username) != -1:
            self.player_number = 2
            zwErg_start = True
        elif self.game.player_one == self.user.username or self.game.player_two == self.user.username:
            async_to_sync(self.channel_layer.group_send)(  # TODO: im Frontend entwickeln
                self.game_id,
                {
                    'type': 'game_reconnect',
                    'username': self.user.username,
                    'target_position': self.game.beer_mug,
                    'player_number': self.player_number,
                    'player_one': self.game.player_one,
                    'player_two': self.game.player_two,
                    'cards': [self.game.cards_player_one, self.game.cards_player_two],
                    'active_player': self.game.get_active_player(),
                    'play_field': self.game.play_field,
                    'brezel_stones': self.game.brezel_stones,
                    'points': self.game.calc_player_points(),
                }
            )
        else:
            return

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.game_id,
            self.channel_name,
        )

        if zwErg_start:
            async_to_sync(self.channel_layer.group_send)(
                self.game_id,
                {
                    'type': 'start_game',
                    'username': self.user.username,
                    'target_position': self.game.beer_mug,
                    'player_number': self.player_number,
                    'player_one': self.game.player_one,
                    'player_two': self.game.player_two,
                    'cards': self.game.game_start(),
                    'active_player': self.game.get_active_player(),
                    'points': self.game.calc_player_points(),
                }
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

        if self.finished:
            return

        if game_message_type == "draw_card":
            if self.game.active_player_number != self.player_number:
                async_to_sync(self.channel_layer.group_send)(
                    self.game_id,
                    {
                        'type': 'game_error',
                        'username': self.user.username,
                        'message': 'Du bist nicht am Zug!',
                    }
                )
                return

            drawn_card = self.game.draw_card(self.player_number)

            if drawn_card == -1:
                async_to_sync(self.channel_layer.group_send)(
                    self.game_id,
                    {
                        'type': 'game_error',
                        'username': self.user.username,
                        'message': 'Du kannst keine Karte mehr ziehen!',
                    }
                )
            else:
                async_to_sync(self.channel_layer.group_send)(
                    self.game_id,
                    {
                        'type': 'draw_card',
                        'username': self.user.username,
                        'player_number': self.player_number,
                        'drawn_card': drawn_card,
                        'active_player': self.game.get_active_player(),
                    }
                )

                self.check_end_of_game()
        elif game_message_type == "play_card":
            if self.game.check_move_possibility(self.player_number, message['card_id']) == 0 and self.game.active_player_number == self.player_number:
                async_to_sync(self.channel_layer.group_send)(
                    self.game_id,
                    {
                        'type': 'play_card',
                        'username': self.user.username,
                        'target_position': self.game.calc_beer_mug_position(self.player_number, message['card_id']),
                        'player_number': self.player_number,
                        'card_id': message['card_id'],
                        'played_card': self.game.play_card(self.player_number, message['card_id'], False),
                        'active_player': self.game.get_active_player(),
                        'brezel_stones': self.game.brezel_stones,
                        'points': self.game.calc_player_points(),
                    }
                )

                self.check_end_of_game()
            elif self.game.active_player_number != self.player_number:
                async_to_sync(self.channel_layer.group_send)(
                    self.game_id,
                    {
                        'type': 'game_error',
                        'username': self.user.username,
                        'message': 'Du bist nicht am Zug!',
                    }
                )
            else:
                async_to_sync(self.channel_layer.group_send)(
                    self.game_id,
                    {
                        'type': 'game_error',
                        'username': self.user.username,
                        'message': 'Diese Karte kann nicht gespielt werden!',
                    }
                )
        elif game_message_type == "play_joker_card":
            if self.game.check_move_possibility(self.player_number, message['card_id']) == 1 and self.game.active_player_number == self.player_number:
                async_to_sync(self.channel_layer.group_send)(
                    self.game_id,
                    {
                        'type': 'play_joker_card',
                        'username': self.user.username,
                        'target_position': self.game.calc_beer_mug_position(self.player_number, message['card_id']),
                        'player_number': self.player_number,
                        'card_id': message['card_id'],
                        'played_card': self.game.play_card(self.player_number, message['card_id'], True),
                        'active_player': self.game.get_active_player(),
                        'brezel_stones': self.game.brezel_stones,
                        'joker_player_one': self.game.joker_player_one,
                        'joker_player_two': self.game.joker_player_two,
                        'points': self.game.calc_player_points(),
                    }
                )

                self.check_end_of_game()
            elif self.game.active_player_number != self.player_number:
                async_to_sync(self.channel_layer.group_send)(
                    self.game_id,
                    {
                        'type': 'game_error',
                        'username': self.user.username,
                        'message': 'Du bist nicht am Zug!',
                    }
                )
            else:
                async_to_sync(self.channel_layer.group_send)(
                    self.game_id,
                    {
                        'type': 'game_error',
                        'username': self.user.username,
                        'message': 'Diese Karte kann nicht gespielt werden!',
                    }
                )
        elif game_message_type == "check_move":
            move_possibility = self.game.check_move_possibility(self.player_number, message['card_id'])

            if self.game.active_player_number != self.player_number:
                async_to_sync(self.channel_layer.group_send)(
                    self.game_id,
                    {
                        'type': 'game_error',
                        'username': self.user.username,
                        'message': 'Du bist nicht am Zug!',
                    }
                )
            elif move_possibility in [0, 1]:
                async_to_sync(self.channel_layer.group_send)(
                    self.game_id,
                    {
                        'type': 'check_move',
                        'username': self.user.username,
                        'target_position': self.game.calc_beer_mug_position(self.player_number, message['card_id']),
                        'player_number': self.player_number,
                        'card_id': message['card_id'],
                        'possible': True,
                        'joker_use': True if move_possibility == 1 else False,
                    }
                )

                self.check_end_of_game()
            else:
                async_to_sync(self.channel_layer.group_send)(
                    self.game_id,
                    {
                        'type': 'check_move',
                        'username': self.user.username,
                        'target_position': self.game.calc_beer_mug_position(self.player_number, message['card_id']),
                        'player_number': self.player_number,
                        'card_id': message['card_id'],
                        'possible': False,
                    }
                )

                self.check_end_of_game()
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.game_id,
                {
                    'type': 'game_error',
                    'username': self.user.username,
                    'message': 'Unbekannte Aktion!',
                }
            )

    def check_end_of_game(self):
        zwErg_end_of_game = self.game.check_for_end_of_game()

        if zwErg_end_of_game != -1:
            async_to_sync(self.channel_layer.group_send)(
                self.game_id,
                {
                    'type': 'game_over',
                    'username': zwErg_end_of_game,
                    'player_one': self.game.player_one,
                    'player_two': self.game.player_two,
                    'points': self.game.calc_player_points(),
                }
            )

            self.finished = True

            BrezelWar.objects.create(game_id=self.game.game_id,
                                     player_one_username=self.game.player_one,
                                     player_two_username=self.game.player_two,
                                     player_one_points=self.game.points_player_one,
                                     player_two_points=self.game.points_player_two,
                                     started_at=self.game.game_start_time,
                                     steps=self.game.steps)

    def start_game(self, event):
        self.send(text_data=json.dumps(event))

    def draw_card(self, event):
        self.send(text_data=json.dumps(event))

    def play_card(self, event):
        self.send(text_data=json.dumps(event))

    def play_joker_card(self, event):
        self.send(text_data=json.dumps(event))

    def check_move(self, event):
        self.send(text_data=json.dumps(event))

    def game_over(self, event):
        self.send(text_data=json.dumps(event))

    def game_error(self, event):
        self.send(text_data=json.dumps(event))

    def game_reconnect(self, event):
        self.send(text_data=json.dumps(event))
