from random import choice

from enums import ResourceType, PlayerSides

CARD_DEFINITIONS = {
    # building cards
    "zed": {
        "price_type": ResourceType.building,
        "price": 1,
        "actions": [
            (PlayerSides.player_on_turn, "add_wall", 3)
        ]
    },

    "zaklady": {
        "price_type": ResourceType.building,
        "price": 1,
        "actions": [
            (PlayerSides.player_on_turn, "add_castle", 2)
        ]
    },

    "vez": {
        "price_type": ResourceType.building,
        "price": 5,
        "actions": [
            (PlayerSides.player_on_turn, "add_castle", 5)
        ]
    },

    "obrana": {
        "price_type": ResourceType.building,
        "price": 3,
        "actions": [
            (PlayerSides.player_on_turn, "add_wall", 6)
        ]
    },

    "hradba": {
        "price_type": ResourceType.building,
        "price": 12,
        "actions": [
            (PlayerSides.player_on_turn, "add_wall", 22)
        ]
    },

    "skola": {
        "price_type": ResourceType.building,
        "price": 8,
        "actions": [
            (PlayerSides.player_on_turn, "add_worker", ResourceType.building)
        ]
    },

    "rezervy": {
        "price_type": ResourceType.building,
        "price": 3,
        "actions": [
            (PlayerSides.player_on_turn, "add_castle", 8),
            (PlayerSides.player_on_turn, "remove_wall", 4)
        ]
    },

    "povoz": {
        "price_type": ResourceType.building,
        "price": 10,
        "actions": [
            (PlayerSides.player_on_turn, "add_castle", 8),
            (PlayerSides.opponent, "attack_castle", 4)
        ]
    },

    "pevnost": {
        "price_type": ResourceType.building,
        "price": 18,
        "actions": [
            (PlayerSides.player_on_turn, "add_castle", 20)
        ]
    },

    "babylon": {
        "price_type": ResourceType.building,
        "price": 39,
        "actions": [
            (PlayerSides.player_on_turn, "add_castle", 32)
        ]
    },

    # army cards
    "ceta": {
        "price_type": ResourceType.army,
        "price": 4,
        "actions": [
            (PlayerSides.opponent, "attack_player", 6)
        ]
    },

    "jezdec": {
        "price_type": ResourceType.army,
        "price": 2,
        "actions": [
            (PlayerSides.opponent, "attack_player", 4)
        ]
    },

    "nabor": {
        "price_type": ResourceType.army,
        "price": 8,
        "actions": [
            (PlayerSides.player_on_turn, "add_worker", ResourceType.army)
        ]
    },

    "rytir": {
        "price_type": ResourceType.army,
        "price": 2,
        "actions": [
            (PlayerSides.opponent, "attack_player", 3)
        ]
    },

    "saboter": {
        "price_type": ResourceType.army,
        "price": 12,
        "actions": [
            (
                PlayerSides.opponent, "remove_material", ResourceType.building,
                4),
            (PlayerSides.opponent, "remove_material", ResourceType.army, 4),
            (PlayerSides.opponent, "remove_material", ResourceType.magic, 4)
        ]
    },

    "smrtka": {
        "price_type": ResourceType.army,
        "price": 28,
        "actions": [
            (PlayerSides.opponent, "attack_player", 32)
        ]
    },

    "strelec": {
        "price_type": ResourceType.army,
        "price": 1,
        "actions": [
            (PlayerSides.opponent, "attack_player", 2)
        ]
    },

    "swat": {
        "price_type": ResourceType.army,
        "price": 18,
        "actions": [
            (PlayerSides.opponent, "attack_castle", 10)
        ]
    },

    # TODO
    # ZLODEJ chybi, je potreba checknout kolik muze ukrast,
    # nejde to primo naimplementovat v aktualnim stavu
    "zlodej": {
        "price_type": ResourceType.army,
        "price": 15
    },

    "ztec": {
        "price_type": ResourceType.army,
        "price": 10,
        "actions": [
            (PlayerSides.opponent, "attack_player", 12)
        ]
    },

    # magic

    "carodej": {
        "price_type": ResourceType.magic,
        "price": 8,
        "actions": [
            (PlayerSides.player_on_turn, "add_worker", ResourceType.magic)
        ]
    },

    "caruj_cihly": {
        "price_type": ResourceType.magic,
        "price": 4,
        "actions": [
            (PlayerSides.player_on_turn, "add_material", ResourceType.building, 8)
        ]
    },

    "caruj_zbrane": {
        "price_type": ResourceType.magic,
        "price": 4,
        "actions": [
            (PlayerSides.player_on_turn, "add_material", ResourceType.army, 8)
        ]
    },

    "caruj_krystaly": {
        "price_type": ResourceType.magic,
        "price": 4,
        "actions": [
            (PlayerSides.player_on_turn, "add_material", ResourceType.magic, 8)
        ]
    },

    "drak": {
        "price_type": ResourceType.magic,
        "price": 21,
        "actions": [
            (PlayerSides.opponent, "attack_player", 25)
        ]
    },

    "kletba": {
        "price_type": ResourceType.magic,
        "price": 25,
        "actions": [
            (PlayerSides.player_on_turn, "add_worker", ResourceType.building),
            (PlayerSides.player_on_turn, "add_material", ResourceType.building, 1),
            (PlayerSides.player_on_turn, "add_worker", ResourceType.army),
            (PlayerSides.player_on_turn, "add_material", ResourceType.army, 1),
            (PlayerSides.player_on_turn, "add_worker", ResourceType.magic),
            (PlayerSides.player_on_turn, "add_material", ResourceType.magic, 1),
            (PlayerSides.player_on_turn, "add_castle", 1),
            (PlayerSides.player_on_turn, "add_wall", 1),

            (PlayerSides.opponent, "remove_worker", ResourceType.building),
            (PlayerSides.opponent, "remove_material", ResourceType.building, 1),
            (PlayerSides.opponent, "remove_worker", ResourceType.army),
            (PlayerSides.opponent, "remove_material", ResourceType.army, 1),
            (PlayerSides.opponent, "remove_worker", ResourceType.magic),
            (PlayerSides.opponent, "remove_material", ResourceType.magic, 1),
            (PlayerSides.opponent, "attack_castle", 1),
            (PlayerSides.opponent, "remove_wall", 1)
        ]
    },

    "skritci": {
        "price_type": ResourceType.magic,
        "price": 22,
        "actions": [
            (PlayerSides.player_on_turn, "add_castle", 22)
        ]
    },

    "znic_cihly": {
        "price_type": ResourceType.magic,
        "price": 4,
        "actions": [
            (PlayerSides.opponent, "remove_material", ResourceType.building, 8)
        ]
    },

    "znic_zbrane": {
        "price_type": ResourceType.magic,
        "price": 4,
        "actions": [
            (PlayerSides.opponent, "remove_material", ResourceType.army, 8)
        ]
    },

    "znic_krystaly": {
        "price_type": ResourceType.magic,
        "price": 4,
        "actions": [
            (PlayerSides.opponent, "remove_material", ResourceType.magic, 8)
        ]
    }
}


def generate_card() -> str:
    return choice(list(CARD_DEFINITIONS.keys()))
