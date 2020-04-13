import json
from typing import Dict
from random import randrange


from enums import ResourceType, PlayerSides
from cards import CARD_DEFINITIONS
from player_status import PlayerStatus


class Game():
    player_1_status = {}
    player_2_status = {}
    __turns = []
    game_status = None
    last_played_card = None

    def __init__(self, player_name: str) -> None:
        self.player_1_status = PlayerStatus(player_name)
        self.game_status = "created"


    def add_second_player(self, player_name: str) -> bool:
        if player_name != self.player_1_status.name:
            self.player_2_status = PlayerStatus(player_name)

            # todo change game status to the first one on the go
            self.game_status = self.player_1_status.name \
                if randrange(2) else self.player_2_status.name
            return True

        return False


    def change_turn(self):
        self.game_status = self.player_1_status.name \
            if self.game_status == self.player_2_status.name else self.player_2_status.name


    def get_player_on_turn(self) -> PlayerStatus:
        return self.player_1_status \
            if self.player_1_status.name == self.game_status else self.player_2_status


    def get_opponent(self) -> PlayerStatus:
        return self.player_2_status \
            if self.player_1_status.name == self.game_status else self.player_1_status


    def play_card(self, card: Dict):
        player_on_turn = self.get_player_on_turn()
        opponent = self.get_opponent()

        # pay for card
        player_on_turn.remove_material(card["price_type"], card["price"])

        for action in card["actions"]:
            args = list(action)[2:]
            if action[0] == PlayerSides.player_on_turn:
                getattr(player_on_turn, action[1])(*args)
            else:
                getattr(opponent, action[1])(*args)


    def play_zlodej(self):
        player_on_turn = self.get_player_on_turn()
        opponent = self.get_opponent()

        # pay for card
        player_on_turn.remove_material(ResourceType.army, 15)

        stolen_resources = opponent.perform_zlodej()
        player_on_turn.add_material(ResourceType.building, stolen_resources[ResourceType.building])
        player_on_turn.add_material(ResourceType.army, stolen_resources[ResourceType.army])
        player_on_turn.add_material(ResourceType.magic, stolen_resources[ResourceType.magic])


    def material_update(self, player_name):
        player = self.get_player_by_name(player_name)
        player.material_update()


    def can_player_play_card(self, player_name: str, card: Dict) -> bool:
        player = self.get_player_by_name(player_name)

        return player.stats[ResourceType(card["price_type"])]["material"] >= card["price"]


    def get_playable_cards(self, player_name):
        player = self.get_player_by_name(player_name)

        playable = []
        for _, card in enumerate(player.hand):
            playable.append(self.can_player_play_card(player_name, CARD_DEFINITIONS[card]))
        return playable


    def is_over(self):
        if self.player_1_status.stats[ResourceType.estate]['castle'] <= 0 or self.player_2_status.stats[ResourceType.estate]['castle'] >= 100:
            return self.player_2_status.name
        elif self.player_2_status.stats[ResourceType.estate]['castle'] <= 0 or self.player_1_status.stats[ResourceType.estate]['castle'] >= 100:
            return self.player_1_status.name
        else:
            return False


    def get_player_by_name(self, player_name):
        player = self.player_1_status if self.player_1_status.name == player_name \
            else self.player_2_status
        return player


    def get_state(self, dump=True):
        player_1_status = dict()
        player_1_status['name'] = self.player_1_status.name

        player_1_status['stats'] = dict()
        player_1_status['stats']['building'] = self.player_1_status.stats[ResourceType.building]
        player_1_status['stats']['army'] = self.player_1_status.stats[ResourceType.army]
        player_1_status['stats']['magic'] = self.player_1_status.stats[ResourceType.magic]
        player_1_status['stats']['estate'] = self.player_1_status.stats[ResourceType.estate]
        player_1_status['hand'] = self.player_1_status.hand

        player_2_status = dict()
        player_2_status['name'] = self.player_2_status.name

        player_2_status['stats'] = dict()
        player_2_status['stats']['building'] = self.player_2_status.stats[ResourceType.building]
        player_2_status['stats']['army'] = self.player_2_status.stats[ResourceType.army]
        player_2_status['stats']['magic'] = self.player_2_status.stats[ResourceType.magic]
        player_2_status['stats']['estate'] = self.player_2_status.stats[ResourceType.estate]
        player_2_status['hand'] = self.player_2_status.hand

        if dump:
            return self.game_status, json.dumps(player_1_status), json.dumps(player_2_status)
        else:
            return self.game_status, self.last_played_card, player_1_status, player_2_status
