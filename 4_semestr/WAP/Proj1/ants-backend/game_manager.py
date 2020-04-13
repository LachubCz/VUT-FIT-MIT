from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from random import randrange

from database import Base, State
from game import Game
from cards import CARD_DEFINITIONS, generate_card


class GameManager():
    __games = {}

    def __init__(self, database_path):
        engine = create_engine('sqlite:///{}' .format(database_path),
                               convert_unicode=True,
                               connect_args={'check_same_thread': False})
        self.db_session = scoped_session(sessionmaker(autocommit=False,
                                                 autoflush=False,
                                                 bind=engine))
        Base.query = self.db_session.query_property()
        Base.metadata.create_all(bind=engine)


    def create_new_game(self, player: str) -> str:
        game_id = self.__generate_game_id(player)
        self.__games[game_id] = Game(player)
        return game_id


    def join_game(self, game_id: str, player_name: str):
        if not self.__does_game_exist(game_id):
            # todo exception type
            raise Exception("requested game doesn't exist")

        elif self.__get_game_status(game_id) != "created":
            # todo exception type
            raise Exception("game has already 2 players")

        elif not self.__is_name_unique_in_game(game_id, player_name):
            # todo exception type
            raise Exception("player name already taken in that game")

        else:
            self.__games[game_id].add_second_player(player_name)


    def play_card(self, game_id: str, player_name: str, card_idx: int):
        # check if game exists + status
        if not self.__does_game_exist(game_id):
            # todo exception type
            raise Exception("requested game doesn't exist")

        if self.__get_game_status(game_id) == "created":
            # todo exception type
            raise Exception("game has not started - waiting for the second player")

        # assign it to variable
        curr_game = self.__games[game_id]
        player = curr_game.get_player_by_name(player_name)
        card_name = player.hand[card_idx]
        card = CARD_DEFINITIONS[card_name]
        # check if its his turn
        if curr_game.game_status != player_name:
            # todo exception type
            raise Exception("it is not " + player_name + "\'s turn")

        # check if player has material to play the card
        if not curr_game.can_player_play_card(player_name, card):
            # todo exception type
            raise Exception("player cannot afford such card")

        # save state to database
        game_status, player_1_status, player_2_status = curr_game.get_state()
        state = State(game_id, game_status, player_1_status, player_2_status, 0, card_name)
        self.add_turn(state)

        # play card
        curr_game.last_played_card = [player.hand[card_idx], 'played']
        if card_name == "zlodej":
            curr_game.play_zlodej()
        else:
            curr_game.play_card(card)

        curr_game.change_turn()
        player.hand[card_idx] = generate_card()

        # checking end of game
        over = curr_game.is_over()
        if over:
            return over
        else:
            return False


    def throw_away_card(self, game_id: str, player_name: str, card_idx: int):
        # check if game exists + status
        if not self.__does_game_exist(game_id):
            # todo exception type
            raise Exception("requested game doesn't exist")

        if self.__get_game_status(game_id) == "created":
            # todo exception type
            raise Exception("game has not started - waiting for the second player")

        # assign it to variable
        curr_game = self.__games[game_id]
        player = curr_game.get_player_by_name(player_name)
        card_name = player.hand[card_idx]

        if curr_game.game_status != player_name:
            # todo exception type
            raise Exception("it is not " + player_name + "\'s turn")

        # save state to database
        game_status, player_1_status, player_2_status = curr_game.get_state()
        state = State(game_id, game_status, player_1_status, player_2_status, 1, card_name)
        self.add_turn(state)

        # throw away card
        curr_game.last_played_card = [player.hand[card_idx], 'thrown_away']
        player.hand[card_idx] = generate_card()
        curr_game.change_turn()


    def material_update(self, game_id, player_name):
        curr_game = self.__games[game_id]
        curr_game.material_update(player_name)


    def is_game_over(self, game_id):
        return self.__games[game_id].is_over()


    def get_game_state(self, game_id, player_name):
        game_status, last_played_card, player_1_status, player_2_status = self.__games[game_id].get_state(dump=False)
        playable = self.__games[game_id].get_playable_cards(player_name)

        player_1_status['hand'] = list(zip(player_1_status['hand'], playable))
        player_2_status['hand'] = list(zip(player_2_status['hand'], playable))

        if player_name == player_1_status['name']:
            player_2_status['hand'] = []
        elif player_name == player_2_status['name']:
            player_1_status['hand'] = []

        state = dict()
        state['game_status'] = game_status
        state['last_played_card'] = last_played_card
        state['player_1_status'] = player_1_status
        state['player_2_status'] = player_2_status

        return state


    def add_turn(self, state):
        self.db_session.add(state)
        self.db_session.commit()


    def __generate_game_id(self, player: str) -> str:
        id = player + str(randrange(9999))
        while id in self.__games.keys():
            id = player + str(randrange(9999))
        return id


    def __does_game_exist(self, game_id: str) -> bool:
        return game_id in self.__games.keys()


    def __get_game_status(self, game_id: str) -> str:
        if self.__does_game_exist(game_id):
            return self.__games[game_id].game_status

        return None


    def __is_name_unique_in_game(self, game_id: str, name: str) -> bool:
        return self.__games[game_id].player_1_status.name != name
