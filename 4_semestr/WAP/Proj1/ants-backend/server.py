import asyncio
import websockets
import configparser

from game_manager import GameManager
from msg import Message


class Server():
    def __init__(self, database_path):
        self.ganager = GameManager(database_path)
        self.websockets = {}
        self.players = {}
        self.ready = {}
        self.first_round = {}


    def process_message(self, msg_string, websocket):
        msg = Message()
        msg.from_json(msg_string)

        if msg.get_msg_name() == 'create_game':
            game_id = self.ganager.create_new_game(player=msg.content)
            self.websockets[game_id] = [websocket]
            self.players[game_id] = [msg.content]
            self.ready[game_id] = False
            new_msg = Message('game_id', game_id, game_id)
            return new_msg.to_json(), game_id

        if msg.get_msg_name() == 'join_game':
            self.ganager.join_game(game_id=msg.game_id, player_name=msg.content)
            self.websockets[msg.game_id].append(websocket)
            self.players[msg.game_id].append(msg.content)
            self.ready[msg.game_id] = True
            new_msg = Message('game_id', msg.game_id, msg.game_id)
            return new_msg.to_json(), msg.game_id

        if msg.get_msg_name() == 'action':
            player_name = self.get_player_name_by_websocket(websocket, msg.game_id)
            end = self.ganager.play_card(game_id=msg.game_id, player_name=player_name, card_idx=msg.content)
            messages = []
            if not end:
                for _, player_name in enumerate(self.players[msg.game_id]):
                    game_state = self.ganager.get_game_state(msg.game_id, player_name)
                    new_msg = Message('state', game_state, msg.game_id)
                    new_msg_str = new_msg.to_json()
                    messages.append(new_msg_str)
            else:
                for _, player_name in enumerate(self.players[msg.game_id]):
                    game_state = self.ganager.get_game_state(msg.game_id, player_name)
                    game_state['game_status'] = end
                    new_msg = Message('end', game_state, msg.game_id)
                    new_msg_str = new_msg.to_json()
                    messages.append(new_msg_str)

            return messages, msg.game_id

        if msg.get_msg_name() == 'throw_away':
            player_name = self.get_player_name_by_websocket(websocket, msg.game_id)
            self.ganager.throw_away_card(game_id=msg.game_id, player_name=player_name, card_idx=msg.content)
            messages = []
            for _, player_name in enumerate(self.players[msg.game_id]):
                game_state = self.ganager.get_game_state(msg.game_id, player_name)
                new_msg = Message('state', game_state, msg.game_id)
                new_msg_str = new_msg.to_json()
                messages.append(new_msg_str)
            return messages, msg.game_id


    def get_player_name_by_websocket(self, websocket, game_id):
        player_name = self.players[game_id][self.websockets[game_id].index(websocket)]
        return player_name


    async def process(self, websocket, path):
        # initial connection
        msg_string = await websocket.recv()
        new_msg_string, game_id = self.process_message(msg_string, websocket)
        await websocket.send(new_msg_string)

        # wait for both player to be connected
        while not self.ready[game_id]:
            await asyncio.sleep(1)

        # initial game state
        player_name = self.get_player_name_by_websocket(websocket, game_id)
        game_state = self.ganager.get_game_state(game_id, player_name)

        new_msg = Message('state', game_state, game_id)

        new_msg_string = new_msg.to_json()
        await websocket.send(new_msg_string)

        # communication
        self.first_round[game_id] = True
        while not self.ganager.is_game_over(game_id):
            msg_string = await websocket.recv()
            new_msgs_strings, game_id = self.process_message(msg_string, websocket)

            for i, websock in enumerate(self.websockets[game_id]):
                await websock.send(new_msgs_strings[i])

                if not self.first_round[game_id]:
                    if not self.ganager.is_game_over(game_id):
                        player_name = None
                        wrong_player = self.get_player_name_by_websocket(websocket, game_id)
                        if self.players[game_id][0] == wrong_player:
                            player_name = self.players[game_id][1]
                        elif self.players[game_id][1] == wrong_player:
                            player_name = self.players[game_id][0]

                        if i == 0:
                            self.ganager.material_update(game_id, player_name)

                        game_state = self.ganager.get_game_state(game_id, player_name)
                        new_msg = Message('material_update', game_state, game_id)
                        new_msg_string = new_msg.to_json()
                        await websock.send(new_msg_string)

            self.first_round[game_id] = False


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.ini")

    server = Server(config['SERVER']['database'])
    print("Database loaded.")
    start_server = websockets.serve(server.process, config['SERVER']['address'], config['SERVER']['port'])

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
