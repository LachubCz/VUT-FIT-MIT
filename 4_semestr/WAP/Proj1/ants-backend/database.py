from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class State(Base):
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer)
    status = Column(String)
    player_1 = Column(String)
    player_2 = Column(String)
    type_of_action = Column(Integer)
    action = Column(String)

    def __init__(self, game_id, status, player_1, player_2, type_of_action, action):
        self.game_id = game_id
        self.status = status
        self.player_1 = player_1
        self.player_2 = player_2
        self.type_of_action = type_of_action
        self.action = action
