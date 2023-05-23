#Importamos deque para aniadir elementos a una coleccion
from collections import deque
from flask import render_template, redirect, Flask, session, request
from flask_socketio import emit, join_room, leave_room, SocketIO, leave_room, join_room
from helpers import login_required

app= Flask(__name__)
app.config["SECRET_KEY"]= "Secret Key"
socketio = SocketIO(app)

channelsCreated = []
UsersLooged = []
channelsMessages = dict()

channelsCreated.append('Public')
channelsMessages['Public'] = deque()

 
#Ruta principal
@app.route('/')
@login_required
def index():
    return render_template("index.html", channels=channelsCreated)

@app.route("/inicio", methods=['GET', 'POST'])
def inicio():
    session.clear()

    username = request.form.get("username")
    if request.method == "POST":
            if username in  UsersLooged:
                 return render_template("warning.html", message="")
            
            UsersLooged.append(username)

            session['username'] = username

            #Recordamos el inicio de sesion
            session.permanent = True

            return redirect("/channels/Public")
    else:
            return render_template("inicio.html")
