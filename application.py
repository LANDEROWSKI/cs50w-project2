

from collections import deque
from flask import Flask, render_template, session, request, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room

from helpers import login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = "Secret key"
socketio = SocketIO(app)

channelsCreated = []
usersLogged = []
channelsMessages = dict()

channelsCreated.append('Public')
channelsMessages['Public'] = deque()

@app.route("/")
@login_required
def index():
    return render_template("index.html", channels=channelsCreated)

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    session.clear()
    username = request.form.get("username")
    if request.method == "POST":
        if username in usersLogged:
            return render_template("warning.html", message="Error")
        usersLogged.append(username)
        session['username'] = username
        session.permanent = True

        return redirect("/channels/Public")
    else:
        return render_template("inicio.html")


@app.route("/change", methods=['GET', 'POST'])
@login_required
def change():
    username = request.form.get("username")
    try:
        usersLogged.remove(session['username'])
    except ValueError:
        pass
    if request.method == "POST":
        if username in usersLogged:
            return render_template("warning.html", message="¡Usuario ya existe!")
        usersLogged.append(username)
        session['username'] = username
        return redirect("/channels/Public")
    else:
        return render_template("modificacion.html", channels=channelsCreated)

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():

    try:
        usersLogged.remove(session['username'])
    except ValueError:
        pass
    return redirect("/signin")

@app.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    newChannel = request.form.get("channel")
    if request.method == "POST":
        if newChannel in channelsCreated:
            return render_template("warning.html", message="¡Este canal ya existe!", channels=channelsCreated)
        channelsCreated.append(newChannel)
        channelsMessages[newChannel] = deque()
        return redirect("/channels/" + newChannel)
    else:
        return render_template("create.html", channels=channelsCreated)

@app.route("/channels/<string:channel>", methods=['GET', 'POST'])
@login_required
def enter_channel(channel):
    user = session['username']
    session['current_channel'] = channel
    if channel not in channelsCreated:
        return redirect("/channels/Public")
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("channel.html", channels=channelsCreated, messages=channelsMessages[channel], usersLogged=usersLogged, user=user)

@socketio.on("joined")
def joined():
    room = session.get('current_channel')
    join_room(room)
    emit('status', {
        'userJoined': session.get('username'),
        'channel': room,
        'msg': str(session.get('username')) + ' ha aterrizado a la partida.'},
        room=room)

@socketio.on('send message')
def send_msg(msg, timestamp):
    room = session.get('current_channel')
    channelsMessages[room].append([timestamp, session.get('username'), msg])
    emit('announce message', {
        'user': session.get('username'),
        'timestamp': timestamp,
        'msg': msg},
        room=room)

@socketio.on("exit")
def exit():
    print("Recent Signal")
    room = session.get('current_channel')

    leave_room(room)

    emit('status', {
        'msg': str(session.get('username')) + ' ha abandonado el canal'},
        room=room)
if __name__ == "__main__":
    socketio.run(app)