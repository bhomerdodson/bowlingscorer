import functools
import sqlite3

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from ..flaskr.db import get_db

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
        row = db.execute('SELECT max(id) as max FROM games').fetchone()
        return jsonify(status=200,game_id=row['max'])
    except sqlite3.Error as error:
        error_string = "Failed to insert new game. Error - {}".format(error)
        return jsonify(status=500,description=error_string), 500
    return jsonify(status=500, description='Failed to do anything'), 500

@bp.route('/add_player', methods=['POST'])
def add_player():
    name = request.form['name']
    game_id = request.form['game_id']
    db = get_db()
    
    try:
        if not name:
            return jsonify(status=400,description='Did not give name of player'), 400
        elif not game_id:
            return jsonify(status=400,description='Did not give game id'), 400
        else:
            row = db.execute('SELECT count(*) as count FROM games WHERE id = ?', (game_id,)).fetchone()
            if row['count'] < 1:
                return jsonify(status=400,description='Game does not exist'), 400
            db.execute('INSERT INTO players (game_id, name) VALUES (?, ?)', (game_id, name))
            db.commit()
            row = db.execute('SELECT id FROM players WHERE game_id = ? AND name = ?', (game_id, name)).fetchone()
            return jsonify(status=200, player_id=row['id']), 200
    except sqlite3.Error as error:
        error_string = "Failed to perform a query. Error - {}".format(error)
        return jsonify(status=500,description=error_string), 500
    return jsonify(status=500,description='Failed to do anything'), 500

@bp.route('/delete_game', methods=['POST'])
def delete_game():
    game_id = request.form['game_id']
    db = get_db()
    
    try:
        if not game_id:
            return jsonify(status=400,description='Did not give game id'), 400
        else:
            row = db.execute('SELECT count(*) as count FROM games WHERE id = ?', (game_id,)).fetchone()
            if row['count'] < 1:
                return jsonify(status=400,description='Game does not exist'), 400
            db.execute('DELETE FROM players WHERE game_id = ?', (game_id,))
            db.execute('DELETE FROM frames WHERE game_id = ?', (game_id,))
            db.execute('DELETE FROM games WHERE id = ?', (game_id,))
            db.commit()
            return jsonify(status=200,description='Successfully deleted game'),200
    except sqlite3.Error as error:
        error_string = "Failed to perform a query. Error - {}".format(error)
        return jsonify(status=500,description=error_string), 500
    return jsonify(status=500,description='Failed to do anything'), 500

@bp.route('/delete_player', methods=['POST'])
def delete_player():
    player_id = request.form['player_id']
    db = get_db()
    
    try:
        if not player_id:
            return jsonify(status=400,description='Did not give game id'), 400
        else:
            row = db.execute('SELECT count(*) as count FROM players WHERE id = ?', (player_id,)).fetchone()
            if row['count'] < 1:
                return jsonify(status=400,description='Player does not exist'), 400
            db.execute('DELETE FROM players WHERE id = ?', (player_id,))
            db.execute('DELETE FROM frames WHERE player_id = ?', (player_id,))
            db.commit()
            return jsonify(status=200,description='Successfully deleted player'),200
    except sqlite3.Error as error:
        error_string = "Failed to perform a query. Error - {}".format(error)
        return jsonify(status=500,description=error_string), 500
    return jsonify(status=500,description='Failed to do anything'), 500
    