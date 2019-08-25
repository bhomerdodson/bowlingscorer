import functools
import sqlite3

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.db import get_db

bp = Blueprint('management', __name__, url_prefix='/management')

@bp.route('/create_game', methods=['POST'])
def create_game():
    name = request.form['name']
    db = get_db()
    
    try:
        if not name:
            db.execute('INSERT INTO games (name) VALUES (?)', ('Game',))
            db.commit()
        else:
            db.execute('INSERT INTO games (name) VALUES (?)', (name,))
            db.commit()
    except sqlite3.Error as error:
        print("Failed to insert new game. Error - {}".format(error))
    return '', 200

@bp.route('/get_games', methods=['GET'])
def get_games():
    db = get_db()
    
    try:
        for row in db.execute('SELECT * FROM games').fetchall():
            print(row['id'])
    except sqlite3.Error as error:
        print("Failed to insert new game. Error - {}".format(error))
    return '', 200

@bp.route('/add_player', methods=['POST'])
def add_player():
    name = request.form['name']
    game_id = request.form['game_id']
    db = get_db()
    
    try:
        if not name:
            return 'Did not give name of player', 400
        elif not game_id:
            return 'Did not give game id', 400
        else:
            row = db.execute('SELECT count(*) as count FROM games WHERE id = ?', (game_id,)).fetchone()
            if row['count'] < 1:
                return 'Game does not exist', 400
            db.execute('INSERT INTO players (game_id, name) VALUES (?, ?)', (game_id, name))
            db.commit()
    except sqlite3.Error as error:
        error_string = "Failed to perform a query. Error - {}".format(error)
        return error_string, 400
    return '', 200

@bp.route('/get_players', methods=['GET'])
def get_players():
    db = get_db()
    
    try:
        for row in db.execute('SELECT * FROM players').fetchall():
            row_vals = [str(row['id']),str(row['game_id']),row['name']]
            print_vals = ", ".join(row_vals)
            print(print_vals)
    except sqlite3.Error as error:
        print("Failed to insert new game. Error - {}".format(error))
    return '', 200

@bp.route('/delete_game', methods=['DELETE'])
def delete_game():
    game_id = request.form['game_id']
    db = get_db()
    
    try:
        if not game_id:
            return 'Did not give game id', 400
        else:
            row = db.execute('SELECT count(*) as count FROM games WHERE id = ?', (game_id,)).fetchone()
            if row['count'] < 1:
                return 'Game does not exist', 400
            db.execute('DELETE FROM players WHERE game_id = ?', (game_id,))
            db.execute('DELETE FROM frames WHERE game_id = ?', (game_id,))
            db.execute('DELETE FROM games WHERE id = ?', (game_id,))
            db.commit()
    except sqlite3.Error as error:
        error_string = "Failed to perform a query. Error - {}".format(error)
        return error_string, 400
    return '', 200

@bp.route('/delete_player', methods=['DELETE'])
def delete_game():
    player_id = request.form['player_id']
    db = get_db()
    
    try:
        if not player_id:
            return 'Did not give game id', 400
        else:
            row = db.execute('SELECT count(*) as count FROM players WHERE id = ?', (player_id,)).fetchone()
            if row['count'] < 1:
                return 'Player does not exist', 400
            db.execute('DELETE FROM players WHERE id = ?', (player_id,))
            db.execute('DELETE FROM frames WHERE player_id = ?', (player_id,))
            db.commit()
    except sqlite3.Error as error:
        error_string = "Failed to perform a query. Error - {}".format(error)
        return error_string, 400
    return '', 200
    