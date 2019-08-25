import os

from flask import Flask
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)
from . import db
db.init_app(app)

@app.route('/hello')
def hello():
    return 'Hello, World!'




#from . import management
#app.register_blueprint(management.manage)

@app.route('/create_game')
def create_game():
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