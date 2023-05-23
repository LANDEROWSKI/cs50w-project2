#Importamos deque para aniadir elementos a una coleccion
from collections import deque
from flask import flask_session, render_template, redirect, Flask, session, request
from flask_socketio import emit, join_room, leave_room, SocketIO, leave_room, join_room
from helpers import login_required

app= Flask(__name__)
app.config["SECRET_KEY"]= "Secret Key"
socketio = SocketIO(app)

channelsCreated = []
UsersLooged = []
channelsMessages = dict()

channelsCreated.append('Public')
channelsMessages['Public'] = deque

 
#Ruta principal
@app.route('/')
@login_required
def index():
    return render_template('index.html', channels = channelsCreated)

@login_required
def home():
    return render_template('iniocio.html',)

#creamos una ruta para el inicio de Sesion
# @app.route('/')