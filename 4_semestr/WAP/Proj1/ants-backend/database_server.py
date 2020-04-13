import json
import configparser
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from database import Base, State

config = configparser.ConfigParser()
config.read("config.ini")

app = Flask(__name__)
engine = create_engine('sqlite:///{}'.format(config['SERVER']['database']),
                       convert_unicode=True,
                       connect_args={'check_same_thread': False})
db_session = scoped_session(sessionmaker(autocommit=False,
                                              autoflush=False,
                                              bind=engine))
Base.query = db_session.query_property()
Base.metadata.create_all(bind=engine)


@app.route('/<from_to>')
def hello_world(from_to):
    from_to = from_to.split('-')
    from_to = list(map(int, from_to))

    if len(from_to) != 2 or from_to[0] > from_to[1] or from_to[0] < 0 or from_to[1] < 0:
        return 'bad_path'

    states = State.query.all()
    records = []
    for i, item in enumerate(states):
        record = dict()
        record['game_id'] = item.game_id
        record['status'] = item.status
        record['player_1'] = json.loads(item.player_1)
        record['player_2'] = json.loads(item.player_2)
        record['type_of_action'] = item.type_of_action
        record['action'] = item.action
        records.append(record)

    records = records[from_to[0]:from_to[1]+1]

    return json.dumps(records)
