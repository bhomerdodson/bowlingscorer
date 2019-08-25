import functools
import sqlite3

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.db import get_db

management = Blueprint('management', __name__, url_prefix='/management')

@management.route('/create_game', methods=('POST'))
def create_game():
    if request.method == 'POST':
        name = request.form['name']
        db = get_db()
        
        try:
            if not name:
                db.execute('INSERT INTO games (name) VALUES (?)', ('Game'))
                db.commit()
            else:
                db.execute('INSERT INTO games (name) VALUES (?)', (name))
                db.commit()
        except sqlite3.Error as error:
            error_message = 'Failed to insert new game' . error