import datetime
import random

active_games = {}


class Game:

    def __init__(self, game_id, user):
        self.game_id = game_id
        self.game_start_time = None
        self.player_one = user
        self.player_two = None
        self.points_player_one = 0
        self.points_player_two = 0
        self.play_field = [[0 for i in range(9)] for i in range(
            9)]  # 1: PlayerOne, 2: PlayerTwo, 3: BeerMug, 4: BeerMug + PlayerOne, 5: BeerMug + PlayerTwo
        self.beer_mug = [4, 4]
        self.brezel_stones = 52
        self.cards_player_one = {}
        self.joker_player_one = 4
        self.cards_player_two = {}
        self.joker_player_two = 4
        self.cards_in_draw_pile = [['N', 1], ['NE', 1], ['E', 1], ['SE', 1], ['S', 1], ['SW', 1], ['W', 1], ['NW', 1],
                                   ['N', 2], ['NE', 2], ['E', 2], ['SE', 2], ['S', 2], ['SW', 2], ['W', 2], ['NW', 2],
                                   ['N', 3], ['NE', 3], ['E', 3], ['SE', 3], ['S', 3], ['SW', 3], ['W', 3], ['NW', 3]]
        self.cards_in_discard_pile = []
        self.steps = ""  # Coded in: <PlayerNumber>_<Kartenquelle>_<KarteRichtung>_<KartenStep>_<Kartenziel>;<NEXTSTEP> TODO: reicht das?
        self.active_player_number = None
        self.random_number = None
        self.current_card_id = None

    def add_player_two(self, user):
        if self.player_two is None and self.player_one != user:
            self.player_two = user
            return user
        else:
            return -1

    def change_active_player(self):
        if self.active_player_number == 1:
            if self.check_possible_moves(2) in [-1, []]:
                return

            self.active_player_number = 2
        else:
            if self.check_possible_moves(1) in [-1, []]:
                return

            self.active_player_number = 1

    def get_player_cards(self, player_number):
        if player_number == 1:
            return self.cards_player_one
        elif player_number == 2:
            return self.cards_player_two
        else:
            return -1

    def get_active_player(self):
        if self.active_player_number == 1:
            return self.player_one
        elif self.active_player_number == 2:
            return self.player_two
        else:
            return -1

    def create_random_number(self, stop, start=0, step=1):
        self.random_number = random.randrange(start, stop, step)
        return self.random_number

    def check_move_possibility(self, player_number, card_id):
        player_cards = self.get_player_cards(player_number)
        zwErg_beer_mug = self.calc_beer_mug_position(player_number, card_id)

        if player_cards == -1:
            return -1

        if zwErg_beer_mug == -1:
            return -1

        if player_number == 1:
            opponent_player_number = 2
        elif player_number == 2:
            opponent_player_number = 1
        else:
            return -1

        if len(player_cards) == 0:
            return -1

        if not (0 <= zwErg_beer_mug[0] <= 8 and 0 <= zwErg_beer_mug[1] <= 8):
            return -1

        if self.play_field[zwErg_beer_mug[0]][zwErg_beer_mug[1]] == 0:
            return 0
        elif self.play_field[zwErg_beer_mug[0]][zwErg_beer_mug[1]] == opponent_player_number:
            if player_number == 1:
                if self.joker_player_one > 0:
                    return 1
                else:
                    return -1
            elif player_number == 2:
                if self.joker_player_two > 0:
                    return 1
                else:
                    return -1
            else:
                return -1
        else:
            return -1

    def check_possible_moves(self, player_number):
        possible_moves = []
        move_possibility = None
        player_cards = self.get_player_cards(player_number)

        if player_cards == -1:
            return -1

        if player_cards.__len__() < 5:
            possible_moves.append(0)

        if player_cards.__len__() > 0:
            for key, card in player_cards.items():
                move_possibility = self.check_move_possibility(player_number, key)

                if move_possibility == 0:
                    possible_moves.append(key)
                elif move_possibility == 1:
                    possible_moves.append(str(int(key) + 10))

        return possible_moves

    def check_for_end_of_game(self):
        if self.brezel_stones <= 0:
            return self.player_one if self.points_player_one > self.points_player_two else self.player_two

        if self.check_possible_moves(1) == [] and self.check_possible_moves(2) == []:
            return self.player_one if self.points_player_one > self.points_player_two else self.player_two

        return -1

    def calc_beer_mug_position(self, player_number, card_id):
        player_cards = self.get_player_cards(player_number)
        zwErg_beer_mug = self.beer_mug.copy()

        if player_cards == -1:
            return -1

        if card_id not in player_cards.keys():
            return -1

        if player_cards[card_id][0] == 'N':
            zwErg_beer_mug[0] -= player_cards[card_id][1]
        elif player_cards[card_id][0] == 'NE':
            zwErg_beer_mug[0] -= player_cards[card_id][1]
            zwErg_beer_mug[1] += player_cards[card_id][1]
        elif player_cards[card_id][0] == 'E':
            zwErg_beer_mug[1] += player_cards[card_id][1]
        elif player_cards[card_id][0] == 'SE':
            zwErg_beer_mug[0] += player_cards[card_id][1]
            zwErg_beer_mug[1] += player_cards[card_id][1]
        elif player_cards[card_id][0] == 'S':
            zwErg_beer_mug[0] += player_cards[card_id][1]
        elif player_cards[card_id][0] == 'SW':
            zwErg_beer_mug[0] += player_cards[card_id][1]
            zwErg_beer_mug[1] -= player_cards[card_id][1]
        elif player_cards[card_id][0] == 'W':
            zwErg_beer_mug[1] -= player_cards[card_id][1]
        elif player_cards[card_id][0] == 'NW':
            zwErg_beer_mug[0] -= player_cards[card_id][1]
            zwErg_beer_mug[1] -= player_cards[card_id][1]
        else:
            return -1

        return zwErg_beer_mug

    def calc_player_points(self):
        checked_fields = []
        zwErg_player_one_points = 0
        zwErg_player_two_points = 0

        for i in range(9):
            for j in range(9):
                if [i, j] not in checked_fields:
                    if self.play_field[i][j] == 1:
                        zwErg_counter = 1
                        checked_fields += [[i, j]]
                        zwErg_current_fields = [[i, j]]

                        while zwErg_current_fields:
                            k, l = zwErg_current_fields[0]

                            if 0 < k and self.play_field[k - 1][l] == 1 and [k - 1, l] not in checked_fields:
                                zwErg_counter += 1
                                checked_fields += [[k - 1, l]]
                                zwErg_current_fields += [[k - 1, l]]

                            if l < 8 and self.play_field[k][l + 1] == 1 and [k, l + 1] not in checked_fields:
                                zwErg_counter += 1
                                checked_fields += [[k, l + 1]]
                                zwErg_current_fields += [[k, l + 1]]

                            if k < 8 and self.play_field[k + 1][l] == 1 and [k + 1, l] not in checked_fields:
                                zwErg_counter += 1
                                checked_fields += [[k + 1, l]]
                                zwErg_current_fields += [[k + 1, l]]

                            if 0 < l and self.play_field[k][l - 1] == 1 and [k, l - 1] not in checked_fields:
                                zwErg_counter += 1
                                checked_fields += [[k, l - 1]]
                                zwErg_current_fields += [[k, l - 1]]

                            zwErg_current_fields.pop(0)

                        zwErg_player_one_points += zwErg_counter ** 2
                    elif self.play_field[i][j] == 2:
                        zwErg_counter = 1
                        checked_fields += [[i, j]]
                        zwErg_current_fields = [[i, j]]

                        while zwErg_current_fields:
                            k, l = zwErg_current_fields[0]

                            if 0 < k and self.play_field[k - 1][l] == 2 and [k - 1, l] not in checked_fields:
                                zwErg_counter += 1
                                checked_fields += [[k - 1, l]]
                                zwErg_current_fields += [[k - 1, l]]

                            if l < 8 and self.play_field[k][l + 1] == 2 and [k, l + 1] not in checked_fields:
                                zwErg_counter += 1
                                checked_fields += [[k, l + 1]]
                                zwErg_current_fields += [[k, l + 1]]

                            if k < 8 and self.play_field[k + 1][l] == 2 and [k + 1, l] not in checked_fields:
                                zwErg_counter += 1
                                checked_fields += [[k + 1, l]]
                                zwErg_current_fields += [[k + 1, l]]

                            if 0 < l and self.play_field[k][l - 1] == 2 and [k, l - 1] not in checked_fields:
                                zwErg_counter += 1
                                checked_fields += [[k, l - 1]]
                                zwErg_current_fields += [[k, l - 1]]

                            zwErg_current_fields.pop(0)

                        zwErg_player_two_points += zwErg_counter ** 2

        self.points_player_one = zwErg_player_one_points
        self.points_player_two = zwErg_player_two_points

        return [zwErg_player_one_points, zwErg_player_two_points]

    def game_start(self):
        self.game_start_time = datetime.datetime.now()

        for i in range(5):
            self.cards_player_one[(i + 1).__str__()] = self.cards_in_draw_pile[
                self.create_random_number(len(self.cards_in_draw_pile))]
            self.steps += "1_drawpile_" + self.cards_player_one[(i + 1).__str__()][0] + "_" + \
                          str(self.cards_player_one[(i + 1).__str__()][1]) + "_" + "cardsplayerone;"
            self.cards_in_draw_pile.pop(self.random_number)

            self.cards_player_two[(i + 1).__str__()] = self.cards_in_draw_pile[
                self.create_random_number(len(self.cards_in_draw_pile))]
            self.steps += "2_drawpile_" + self.cards_player_two[(i + 1).__str__()][0] + "_" + \
                          str(self.cards_player_two[(i + 1).__str__()][1]) + "_" + "cardsplayertwo;"
            self.cards_in_draw_pile.pop(self.random_number)

        self.active_player_number = 1

        return [self.cards_player_one, self.cards_player_two]

    def draw_card(self, player_number):
        player_cards = self.get_player_cards(player_number)

        if len(self.cards_in_draw_pile) == 0:
            self.cards_in_draw_pile = self.cards_in_discard_pile.copy()
            self.cards_in_discard_pile = []

        if player_cards == -1:
            return -1

        if player_number != self.active_player_number:
            return -1

        if len(player_cards) < 5:
            for i in range(5):
                if (i + 1).__str__() not in player_cards.keys():
                    player_cards[(i + 1).__str__()] = self.cards_in_draw_pile[
                        self.create_random_number(len(self.cards_in_draw_pile))]
                    self.cards_in_draw_pile.pop(self.random_number)
                    self.current_card_id = (i + 1).__str__()

                    if player_number == 1:
                        self.steps += "1_drawpile_" + self.cards_player_one[self.current_card_id][0] + "_" + \
                                      str(self.cards_player_one[self.current_card_id][1]) + "_" + "cardsplayerone;"
                    else:
                        self.steps += "2_drawpile_" + self.cards_player_two[self.current_card_id][0] + "_" + \
                                      str(self.cards_player_two[self.current_card_id][1]) + "_" + "cardsplayertwo;"

                    break
        else:
            return -1

        self.change_active_player()

        return [self.current_card_id, player_cards[self.current_card_id]]

    def play_card(self, player_number, card_id, joker_used=False):
        player_cards = self.get_player_cards(player_number)
        move_possibility = None

        if player_cards == -1:
            return -1

        if player_number != self.active_player_number:
            return -1

        move_possibility = self.check_move_possibility(player_number, card_id)

        if move_possibility == -1:
            return -1

        if move_possibility == 0:
            self.beer_mug = self.calc_beer_mug_position(player_number, card_id)

            self.play_field[self.beer_mug[0]][self.beer_mug[1]] = player_number
        elif move_possibility == 1 and joker_used:
            self.beer_mug = self.calc_beer_mug_position(player_number, card_id)

            self.play_field[self.beer_mug[0]][self.beer_mug[1]] = player_number

            if player_number == 1:
                self.joker_player_one -= 1
            elif player_number == 2:
                self.joker_player_two -= 1
            else:
                return -1
        else:
            return -1

        self.brezel_stones -= 1
        self.cards_in_discard_pile.append(player_cards[card_id])
        player_cards.pop(card_id, None)

        source = "cardsplayerone" if player_number == 1 else "cardsplayertwo"
        self.steps += str(player_number) + "_" + source + "_" + self.cards_in_discard_pile[-1][0] + "_" + \
                      str(self.cards_in_discard_pile[-1][1]) + "_" + "discardpile;"

        self.change_active_player()

        return self.cards_in_discard_pile[-1]
