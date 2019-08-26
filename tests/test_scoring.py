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

def test_add_frame_failures(client, scoring, manage, app):
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
    
    for x in range(10):
        scoring.add_frame(player_id, game_id).data
    
    response = scoring.add_frame(player_id, game_id).data
    result = json.loads(response)
    
    assert result['status'] == 409
    assert result['description'] == 'Cannot add any more frames'
    
    response = manage.add_frame('', game_id).data
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Did not give player id'
    
    response = manage.add_frame(player_id, '').data
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Did not give game id'