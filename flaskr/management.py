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
        elif:
            db.execute('INSERT INTO players (game_id, name) VALUES (?, ?)', (game_id, name))
            db.commit()
    except sqlite3.Error as error:
        error_string = "Failed to perform insert. Error - {}".format(error)
        return error_string, 400
    return '', 200
    