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
    
    response = scoring.add_frame('', game_id).data
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Did not give player id'
    
    response = scoring.add_frame(player_id, '').data
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Did not give game id'

def test_update_frame(client, scoring, manage, app):
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
    
    response = scoring.update_frame(frame_id, 1, 5).data
    result = json.loads(response)
    
    assert result['status'] == 200
    assert result['description'] == 'Updated frame successfully'
    
    with app.app_context():
        row = get_db().execute('SELECT * FROM frames WHERE id = ?', (frame_id,)).fetchone()
        assert row is not None
        assert row['ball_one'] == 5
        assert row['ball_two'] == 0
        assert row['ball_three'] == 0
        assert row['strike'] == 0
        assert row['spare'] == 0
        assert row['total_game_score'] == 5
    
    response = scoring.update_frame(frame_id, 2, 3).data
    result = json.loads(response)
    
    assert result['status'] == 200
    assert result['description'] == 'Updated frame successfully'
    
    with app.app_context():
        row = get_db().execute('SELECT * FROM frames WHERE id = ?', (frame_id,)).fetchone()
        assert row is not None
        assert row['ball_one'] == 5
        assert row['ball_two'] == 3
        assert row['ball_three'] == 0
        assert row['strike'] == 0
        assert row['spare'] == 0
        assert row['total_game_score'] == 8
    
    response = scoring.update_frame(frame_id, 2, 5).data
    result = json.loads(response)
    
    assert result['status'] == 200
    assert result['description'] == 'Updated frame successfully'
    
    with app.app_context():
        row = get_db().execute('SELECT * FROM frames WHERE id = ?', (frame_id,)).fetchone()
        assert row is not None
        assert row['ball_one'] == 5
        assert row['ball_two'] == 5
        assert row['ball_three'] == 0
        assert row['strike'] == 0
        assert row['spare'] == 1
        assert row['total_game_score'] == 10
    
    scoring.update_frame(frame_id, 2, 0).data
    response = scoring.update_frame(frame_id, 1, 10).data
    result = json.loads(response)
    
    assert result['status'] == 200
    assert result['description'] == 'Updated frame successfully'
    
    with app.app_context():
        row = get_db().execute('SELECT * FROM frames WHERE id = ?', (frame_id,)).fetchone()
        assert row is not None
        assert row['ball_one'] == 10
        assert row['ball_two'] == 0
        assert row['ball_three'] == 0
        assert row['strike'] == 1
        assert row['spare'] == 0
        assert row['total_game_score'] == 10

def test_update_frame_failures(client, scoring, manage, app):
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
    
    response = scoring.update_frame('', 1, 4).data
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Did not give a frame id'
    
    response = scoring.update_frame(frame_id, 0, 4).data
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Did not give a valid ball number'
    
    response = scoring.update_frame(frame_id, 4, 4).data
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Did not give a valid ball number'
    
    response = scoring.update_frame(frame_id, 1, -1).data
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Did not give a valid pin count'
    
    response = scoring.update_frame(frame_id, 1, 11).data
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Did not give a valid pin count'
    
    response = scoring.update_frame(frame_id, 1, 5).data
    result = json.loads(response)
    
    assert result['status'] == 200
    assert result['description'] == 'Updated frame successfully'
    
    with app.app_context():
        row = get_db().execute('SELECT * FROM frames WHERE id = ?', (frame_id,)).fetchone()
        assert row is not None
        assert row['ball_one'] == 5
        assert row['ball_two'] == 0
        assert row['ball_three'] == 0
        assert row['strike'] == 0
        assert row['spare'] == 0
        assert row['total_game_score'] == 5
    
    response = scoring.update_frame(frame_id, 2, 6).data
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Too many pins added'
    
    response = scoring.update_frame(frame_id, 3, 6).data
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Tried to update ball 3 on not the tenth frame'
    
    response = scoring.update_frame(5000, 1, 5).data
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Invalid frame id'

def test_perfect_game(client, scoring, manage, app):
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
    
    temp_frame_id = 0
    for x in range(10):
        response = scoring.add_frame(player_id, game_id).data
        result = json.loads(response)
        
        assert result['status'] == 200
        
        frame_id = result['frameid']
        temp_frame_id = result['frameid']
        with app.app_context():
            row = get_db().execute('SELECT count(*) as count FROM frames WHERE id = ?', (frame_id,)).fetchone()
            assert row is not None
            assert row['count'] == 1
        
        response = scoring.update_frame(frame_id, 1, 10).data
        result = json.loads(response)
        
        assert result['status'] == 200
        
        if x == 9:
            response = scoring.update_frame(frame_id, 2, 10).data
            result = json.loads(response)
            
            assert result['status'] == 200
            
            response = scoring.update_frame(frame_id, 3, 10).data
            result = json.loads(response)
            
            assert result['status'] == 200
    
    with app.app_context():
            row = get_db().execute('SELECT total_game_score FROM frames WHERE id = ?', (temp_frame_id,)).fetchone()
            assert row is not None
            assert row['total_game_score'] == 300

def test_spare(client, scoring, manage, app):
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
    
    response = scoring.update_frame(frame_id, 1, 5).data
    result = json.loads(response)
    
    assert result['status'] == 200
    
    response = scoring.update_frame(frame_id, 2, 5).data
    result = json.loads(response)
    
    assert result['status'] == 200
    
    response = scoring.add_frame(player_id, game_id).data
    result = json.loads(response)
    
    assert result['status'] == 200
    
    second_frame_id = result['frameid']
    with app.app_context():
        row = get_db().execute('SELECT count(*) as count FROM frames WHERE id = ?', (second_frame_id,)).fetchone()
        assert row is not None
        assert row['count'] == 1
    
    response = scoring.update_frame(second_frame_id, 1, 5).data
    result = json.loads(response)
    
    assert result['status'] == 200
    
    with app.app_context():
        row = get_db().execute('SELECT total_game_score FROM frames WHERE id = ?', (frame_id,)).fetchone()
        assert row is not None
        assert row['total_game_score'] == 15

def test_get_score(client, scoring, manage, app):
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
    
    response = scoring.update_frame(frame_id, 1, 5).data
    result = json.loads(response)
    
    assert result['status'] == 200
    assert result['description'] == 'Updated frame successfully'
    
    response = scoring.update_frame(frame_id, 2, 3).data
    result = json.loads(response)
    
    assert result['status'] == 200
    assert result['description'] == 'Updated frame successfully'
    
    response = scoring.get_score(frame_id).data
    result = json.loads(response)
    
    assert result['status'] == 200
    assert result['game_score'] == 8

def test_get_score_failures(client, scoring, manage, app):
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
    
    response = scoring.update_frame(frame_id, 1, 5).data
    result = json.loads(response)
    
    assert result['status'] == 200
    assert result['description'] == 'Updated frame successfully'
    
    response = scoring.update_frame(frame_id, 2, 3).data
    result = json.loads(response)
    
    assert result['status'] == 200
    assert result['description'] == 'Updated frame successfully'
    
    response = scoring.get_score('').data
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Did not give a frame id'
    
    response = scoring.get_score(5000).data
    result = json.loads(response)
    
    assert result['status'] == 400
    assert result['description'] == 'Not a valid frame id'

def test_get_frame_info(client, scoring, manage, app):
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
    
    response = scoring.update_frame(frame_id, 1, 5).data
    result = json.loads(response)
    
    assert result['status'] == 200
    assert result['description'] == 'Updated frame successfully'
    
    response = scoring.update_frame(frame_id, 2, 3).data
    result = json.loads(response)
    
    assert result['status'] == 200
    assert result['description'] == 'Updated frame successfully'
    
    response = scoring.get_frame_info(frame_id).data
    result = json.loads(response)
    
    assert result['status'] == 200
    
    assert result['game_id'] == game_id
    assert result['player_id'] == player_id
    assert result['frame_number'] == 1
    assert result['ball_one'] == 5
    assert result['ball_two'] == 3
    assert result['ball_three'] == 0
    assert result['strike'] == 0
    assert result['spare'] == 0
    assert result['total_game_score'] == 8