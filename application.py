from flask import flask_session, render_template, redirect, Flask
from flask_socketio import emit, join_room, leave_room, SocketIO


app= Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def index():
    return render_template('index.html')