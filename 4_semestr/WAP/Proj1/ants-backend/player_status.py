from typing import Dict

from cards import generate_card
from enums import ResourceType


class PlayerStatus:
    name = ""

    def __init__(self, player_name: str):
        self.name = player_name
        self.stats = {}
        self.stats[ResourceType.building] = {
            "workers": 2,
            "material": 5
        }
        self.stats[ResourceType.army] = {
            "workers": 2,
            "material": 5
        }
        self.stats[ResourceType.magic] = {
            "workers": 2,
            "material": 5
        }
        self.stats[ResourceType.estate] = {
            "castle": 30,
            "wall": 10
        }

        # todo HAND
        self.hand = []
        for _ in range(8):
            self.hand.append(generate_card())


    def material_update(self):
        self.stats[ResourceType.building]['material'] += self.stats[ResourceType.building]['workers']
        self.stats[ResourceType.army]['material'] += self.stats[ResourceType.army]['workers']
        self.stats[ResourceType.magic]['material'] += self.stats[ResourceType.magic]['workers']


    def add_worker(self, type: ResourceType):
        self.stats[type]["workers"] += 1


    def add_material(self, type: ResourceType, amount: int):
        self.stats[type]["material"] += amount


    def remove_worker(self, type: ResourceType):
        self.stats[type]["workers"] -= 1
        if self.stats[type]["workers"] < 0:
            self.stats[type]["workers"] = 0


    def remove_material(self, type: ResourceType, amount: int):
        self.stats[type]["material"] -= amount
        if self.stats[type]["material"] < 0:
            self.stats[type]["material"] = 0


    def remove_wall(self, amount: int):
        self.stats[ResourceType.estate]["wall"] -= amount
        if self.stats[ResourceType.estate]["wall"] < 0:
            self.stats[ResourceType.estate]["wall"] = 0


    def attack_player(self, amount: int):
        if self.stats[ResourceType.estate]["wall"] < amount:
            self.attack_castle(amount - self.stats[ResourceType.estate]["wall"])
            self.stats[ResourceType.estate]["wall"] = 0
        else:
            self.stats[ResourceType.estate]["wall"] -= amount


    def attack_castle(self, amount: int):
        self.stats[ResourceType.estate]["castle"] -= amount


    def add_wall(self, amount: int):
        self.stats[ResourceType.estate]["wall"] += amount


    def add_castle(self, amount: int):
        self.stats[ResourceType.estate]["castle"] += amount


    def perform_zlodej(self) -> Dict:
        stolen_goods = {}
        if self.stats[ResourceType.building]["material"] >= 5:
            stolen_goods[ResourceType.building] = 5
        else:
            stolen_goods[ResourceType.building] = self.stats[ResourceType.building]["material"]

        if self.stats[ResourceType.army]["material"] >= 5:
            stolen_goods[ResourceType.army] = 5
        else:
            stolen_goods[ResourceType.army] = self.stats[ResourceType.army]["material"]

        if self.stats[ResourceType.magic]["material"] >= 5:
            stolen_goods[ResourceType.magic] = 5
        else:
            stolen_goods[ResourceType.magic] = self.stats[ResourceType.magic]["material"]

        self.remove_material(ResourceType.building, 5)
        self.remove_material(ResourceType.army, 5)
        self.remove_material(ResourceType.magic, 5)

        return stolen_goods
