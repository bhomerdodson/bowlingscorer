import functools
import sqlite3

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from ..flaskr.db import get_db

bp = Blueprint('scoring', __name__, url_prefix='/scoring')

#Adds a frame associated with a player to a game
#player_id - player the frame is associated with
#game_id - game the frame is associated with
@bp.route('/add_frame', methods=['POST'])
def add_frame():
    player_id = request.form['player_id']
    game_id = request.form['game_id']
    db = get_db()
    
    try:
        if not player_id:
            return jsonify(status=400,description='Did not give player id'), 400
        elif not game_id:
            return jsonify(status=400,description='Did not give game id'), 400
        else:
            row = db.execute('SELECT count(*) as count FROM frames WHERE player_id = ? AND game_id = ?', (player_id, game_id)).fetchone()
            frame_count = row['count']
            if frame_count>9:
                return jsonify(status=409,description='Cannot add any more frames'), 409
            else:
                frame_count = frame_count + 1
                db.execute('INSERT INTO frames (player_id, game_id, frame_number) VALUES (?, ?, ?)', (player_id, game_id, frame_count))
                db.commit()
                row = db.execute('SELECT id FROM frames WHERE player_id = ? AND game_id = ? AND frame_number = ?', (player_id, game_id, frame_count)).fetchone()
                frame_id = row['id']
                return jsonify(frameid=frame_id,status=200), 200
    except sqlite3.Error as error:
        error_string = "Failed to perform a query. Error - {}".format(error)
        return jsonify(status=500,description=error_string), 500
    return jsonify(status=500,description='Failed to do anything'), 500

#Calculates the total game score for the given frame
#frame_id - the frame that is having its score calculated
def calculate_score(frame_id):
    db = get_db()
    
    try:
        row = db.execute('SELECT * FROM frames WHERE id = ?', (frame_id,)).fetchone()
        if row is not None:
            #Get the relevant information from the frame
            game_id = row['game_id']
            player_id = row['player_id']
            frame_number = row['frame_number']
            ball_one = row['ball_one']
            ball_two = row['ball_two']
            ball_three = row['ball_three']
            strike = row['strike']
            spare = row['spare']
            #Temporary variable to hold the game score as it is being calculated
            temp_game_score = 0
            #Get the total game score from previous frames. This should only be done on frames 2-10
            if frame_number>1:
                last_frame = frame_number - 1
                temp_row = db.execute('SELECT id FROM frames WHERE player_id = ? AND game_id = ? AND frame_number = ?', (player_id, game_id, last_frame)).fetchone()
                if temp_row is not None:
                    last_frame_id = temp_row['id']
                    temp_game_score = calculate_score(last_frame_id);
            total_frame_score = ball_one + ball_two + ball_three
            extra_frame_one = frame_number + 1
            extra_frame_two = frame_number + 2
            extra_ball_one = 0
            extra_ball_two = 0
            if strike == 1:
                strike_row = db.execute('SELECT ball_one, ball_two, strike FROM frames WHERE player_id = ? AND game_id = ? AND frame_number = ?', (player_id, game_id, extra_frame_one)).fetchone()
                if strike_row is not None:
                    extra_ball_one = strike_row['ball_one']
                    extra_ball_two = strike_row['ball_two']
                    extra_strike = strike_row['strike']
                    if extra_strike == 1:
                        strike_row = db.execute('SELECT ball_one FROM frames WHERE player_id = ? AND game_id = ? AND frame_number = ?', (player_id, game_id, extra_frame_two)).fetchone()
                        if strike_row is not None:
                            extra_ball_two = strike_row['ball_one']
            elif spare == 1:
                spare_row = db.execute('SELECT ball_one FROM frames WHERE player_id = ? AND game_id = ? AND frame_number = ?', (player_id, game_id, extra_frame_one)).fetchone()
                if spare_row is not None:
                    extra_ball_one = spare_row['ball_one']
            total_frame_score = total_frame_score + extra_ball_one + extra_ball_two
            total_game_score = temp_game_score + total_frame_score
            db.execute('UPDATE frames SET total_game_score = ? WHERE id = ?', (total_game_score, frame_id))
            db.commit()
            return total_game_score
    except sqlite3.Error as error:
        print("Failed to perform a query. Error - {}".format(error))
        return 0
    return 0

#Updates the values for the balls bowled in a frame
#frame_id - The frame being updated
#ball_number - The ball in the frame
#pin_count - The number of pins that were knocked down for the given ball
@bp.route('/update_frame', methods=['POST'])
def update_frame():
    frame_id = request.form['frame_id']
    ball_number = int(request.form['ball_number'])
    pin_count = int(request.form['pin_count'])
    db = get_db();
    
    try:
        if not frame_id:
            return jsonify(status=400,description='Did not give a frame id'), 400
        elif ball_number>3 or ball_number<1:
            return jsonify(status=400,description='Did not give a valid ball number'), 400
        elif pin_count<0 or pin_count>10:
            return jsonify(status=400,description='Did not give a valid pin count'), 400
        else:
            row = db.execute('SELECT * FROM frames WHERE id = ?', (frame_id,)).fetchone()
            if row is not None:
                if ball_number == 3:
                    if row['frame_number'] == 10:
                        db.execute('UPDATE frames SET ball_three = ? WHERE id = ?', (pin_count, frame_id))
                        db.commit()
                    else:
                        return jsonify(status=400,description='Tried to update ball 3 on not the tenth frame'), 400
                elif ball_number == 2:
                    frame_total = row['ball_one'] + pin_count
                    if frame_total>10 and row['frame_number']<10:
                        return jsonify(status=400,description='Too many pins added'), 400
                    elif frame_total == 10:
                        db.execute('UPDATE frames SET ball_two = ?, spare = ?, strike = ? WHERE id = ?', (pin_count, 1, 0, frame_id))
                        db.commit()
                    else:
                        db.execute('UPDATE frames SET ball_two = ?, strike = ?, spare = ? WHERE id = ?', (pin_count, 0, 0, frame_id))
                        db.commit()
                else:
                    if pin_count == 10:
                        db.execute('UPDATE frames SET ball_one = ?, strike = ?, spare = ? WHERE id = ?', (pin_count, 1, 0, frame_id))
                        db.commit()
                    else:
                        db.execute('UPDATE frames SET ball_one = ?, strike = ? WHERE id = ?', (pin_count, 0, frame_id))
                        db.commit()
                calculate_score(frame_id)
            else:
                return jsonify(status=400,description='Invalid frame id'), 400
    except sqlite3.Error as error:
        error_string = "Failed to perform a query. Error - {}".format(error)
        return jsonify(status=500,description=error_string), 500
    return jsonify(status=200,description='Updated frame successfully'), 200

#Gives the total game score for the given frame
#frame_id - The frame to get the score from
@bp.route('/get_score', methods=['POST'])
def get_score():
    frame_id = request.form['frame_id']
    db = get_db()
    
    try:
        if not frame_id:
            return jsonify(status=400,description='Did not give a frame id'), 400
        else:
            row = db.execute('SELECT total_game_score FROM frames WHERE id = ?', (frame_id,)).fetchone()
            if row is not None:
                return jsonify(status=200,game_score=row['total_game_score']), 200
            else:
                return jsonify(status=400,description='Not a valid frame id'), 400
    except sqlite3.Error as error:
        error_string = "Failed to perform a query. Error - {}".format(error)
        return jsonify(status=400,description=error_string), 400
    return jsonify(status=500,description='Failed to do anything'), 500

#Gives all the information from a given frame
#frame_id - The frame to get the information from
@bp.route('/get_frame_info', methods=['POST'])
def get_frame_info():
    frame_id = request.form['frame_id']
    print(frame_id)
    db = get_db()
    
    try:
        if not frame_id:
            return jsonify(status=400,description='Did not give a frame id'), 400
        else:
            row = db.execute('SELECT * FROM frames WHERE id = ?', (frame_id,)).fetchone()
            if row is not None:
                return jsonify(status=200,game_id=row['game_id'], player_id=row['player_id'], frame_number=row['frame_number'], ball_one=row['ball_one'], ball_two=row['ball_two'], ball_three=row['ball_three'], strike=row['strike'], spare=row['spare'], total_game_score=row['total_game_score']), 200
    except sqlite3.Error as error:
        error_string = "Failed to perform a query. Error - {}".format(error)
        return error_string, 400
    return jsonify(status=400,description='Did not give a valid frame id'), 400