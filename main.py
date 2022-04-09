from flask import Flask
from pages import blueprint
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'beta-secret-key'
app.register_blueprint(blueprint)

db_session.global_init("db/music.db")
app.run(host='127.0.0.1')
