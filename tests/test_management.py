import pytest
import json

from flaskr.db import get_db

def test_create_delete_game(client, manage):
    result_json = manage.create_game()
    result = json.loads(result_json)
    
    assert result['status'] == 200
    
    game_id = result['game_id']
    with app.app_context():
        row = get_db().execute('SELECT count(*) as count FROM games WHERE id = ?', (game_id,)).fetchone()
        assert row is not None
        assert row['count'] == 1
    
    result_json = manage.delete_game()
    result = json.loads(result_json)
    
    assert result['status'] == 200
    
    with app.app_context():
        row = get_db().execute('SELECT count(*) as count FROM games WHERE id = ?', (game_id,)).fetchone()
        assert row is not None
        assert row['count'] == 0