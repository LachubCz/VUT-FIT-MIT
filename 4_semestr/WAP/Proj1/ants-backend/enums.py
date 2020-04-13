from enum import Enum


class ResourceType(Enum):
    building = 1
    army = 2
    magic = 3
    estate = 4


class PlayerSides(Enum):
    player_on_turn = 1
    opponent = 2
