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
            print(row)
    except sqlite3.Error as error:
        print("Failed to insert new game. Error - {}".format(error))
    return '', 200