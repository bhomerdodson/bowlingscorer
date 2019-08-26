import pytest
import json

from ..flaskr.db import get_db

def test_add_frame(client, scoring, manage, app):
    response = manage.create_game('Test').data
    result = json.loads(response)
    
    assert result['status'] == 200
    
    game_id = result['game_id']
    with app.app_context():
        row = get_db().execute('SELECT count(*) as count FROM games WHERE id = ?', (game_id,)).fetchone()
        assert row is not None
        assert row['count'] == 1
    
    response = manage.add_player('Ben', game_id).data
    result = json.loads(response)
    
    assert result['status'] == 200
    
    player_id = result['player_id']
    with app.app_context():
        row = get_db().execute('SELECT count(*) as count FROM players WHERE id = ?', (player_id,)).fetchone()
        assert row is not None
        assert row['count'] == 1
    
    response = scoring.add_frame(player_id, game_id).data
    result = json.loads(response)
    
    assert result['status'] == 200
    
    frame_id = result['frameid']
    with app.app_context():
        row = get_db().execute('SELECT count(*) as count FROM frames WHERE id = ?', (frame_id,)).fetchone()
        assert row is not None
        assert row['count'] == 1