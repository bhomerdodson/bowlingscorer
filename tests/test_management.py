import pytest
import json

from ..flaskr.db import get_db

#Tests that the create_game and delete_game rest calls work as expected on good input
def test_create_delete_game(client, manage, app):
    response = manage.create_game('Test').data
    result = json.loads(response)
    
    assert result['status'] == 200
    
    game_id = result['game_id']
    with app.app_context():
        row = get_db().execute('SELECT count(*) as count FROM games WHERE id = ?', (game_id,)).fetchone()
        assert row is not None
        assert row['count'] == 1
    
    response = manage.delete_game(game_id).data
    result = json.loads(response)
    
    assert result['status'] == 200
    
    with app.app_context():
        row = get_db().execute('SELECT count(*) as count FROM games WHERE id = ?', (game_id,)).fetchone()
        assert row is not None
        assert row['count'] == 0

#Tests that the add_player and delete_player rest calls work as expected on good input
def test_create_delete_player(client, manage, app):
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
    
    response = manage.delete_player(player_id).data
    result = json.loads(response)
    
    assert result['status'] == 200
    
    with app.app_context():
        row = get_db().execute('SELECT count(*) as count FROM players WHERE id = ?', (player_id,)).fetchone()
        assert row is not None
        assert row['count'] == 0

#Tests that the add_player rest call works as expected on bad input
def test_add_player_failures(client, manage, app):
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
        
    response = manage.add_player('', game_id).data
    
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Did not give name of player'
    
    response = manage.add_player('Tom', '').data
    
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Did not give game id'
    
    response = manage.add_player('Bart', int(game_id) + 1).data
    
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Game does not exist'

#Tests that the delete_game rest call works as expected on bad input
def test_delete_game_failures(client, manage, app):
    
    response = manage.delete_game('').data
    
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Did not give game id'
    
    response = manage.delete_game(5000).data
    
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Game does not exist'

#Tests that the delete_player rest call works as expected on bad input
def test_delete_player_failures(client, manage, app):
    
    response = manage.delete_player('').data
    
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Did not give player id'
    
    response = manage.delete_player(5000).data
    
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Player does not exist'