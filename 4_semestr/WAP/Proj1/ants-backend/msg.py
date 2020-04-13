import json

class Message():
    type = None
    content = None
    game_id = None

    def __init__(self, type=None, content=None, game_id=None):
        if type is not None:
            self.type = self.get_msg_code(type)
        if content is not None:
            self.content = content
        if game_id is not None:
            self.game_id = game_id


    def to_json(self):
        msg = dict()

        msg['type'] = self.type
        msg['content'] = self.content
        if self.game_id is not None:
            msg['game_id'] = self.game_id

        return json.dumps(msg)


    def from_json(self, json_string):
        msg = json.loads(json_string)

        self.type = msg['type']
        self.content = msg['content']
        if 'game_id' in msg:
            self.game_id = msg['game_id']


    def get_msg_code(self, name):
        if name == 'create_game':
            return 0
        elif name == 'join_game':
            return 1
        elif name == 'game_id':
            return 2
        elif name == 'state':
            return 3
        elif name == 'action':
            return 4
        elif name == 'end':
            return 5
        elif name == 'throw_away':
            return 6
        elif name == 'material_update':
            return 7
        else:
            return -1


    def get_msg_name(self):
        if self.type == 0:
            return 'create_game'
        elif self.type == 1:
            return 'join_game'
        elif self.type == 2:
            return 'game_id'
        elif self.type == 3:
            return 'state'
        elif self.type == 4:
            return 'action'
        elif self.type == 5:
            return 'end'
        elif self.type == 6:
            return 'throw_away'
        elif self.type == 7:
            return 'material_update'
        else:
            return 'bad message'
