import os
import tempfile

import pytest
from tests..flaskr import create_app
from tests..flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })
    
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
    
    yield app
    
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class ScoringCalls(object):
    def __init__(self, client):
        self._client = client
    
    def add_frame(self, player_id=1, game_id=1):
        return self._client.post(
            '/scoring/add_frame',
            data={'player_id': player_id, 'game_id': game_id}
        )
    
    def update_frame(self, frame_id=1, ball_number=1, pin_count=0):
        return self._client.post(
            '/scoring/update_frame',
            data={'frame_id': frame_id, 'ball_number': ball_number, 'pin_count': pin_count}
        )
    
    def get_score(self, frame_id=1):
        return self._client.post(
            '/scoring/get_score',
            data={'frame_id': frame_id}
        )
    
    def get_frame_info(self, frame_id=1):
        return self._client_post(
            '/scoring/get_frame_info',
            data={'frame_id': frame_id}
        )

class ManagementCalls(object):
    def __init__(self, client):
        self._client = client
    
    def create_game(self, name=''):
        return self._client.post(
            '/management/create_game',
            data={'name': name}
        )
    
    def add_player(self, name='Test', game_id='1'):
        return self._client.post(
            '/management/add_player',
            data={'name': name, 'game_id': game_id}
        )
    
    def delete_game(self, game_id='1'):
        return self._client.post(
            '/management/delete_game',
            data={'game_id': game_id}
        )
    
    def delete_player(self, player_id='1'):
        return self._client.post(
            '/management/delete_player',
            data={'player_id', player_id}
        )

@pytest.fixture
def scoring(client):
    return ScoringCalls(client)

@pytest.fixture
def manage(client):
    return ManagementCalls(client)
