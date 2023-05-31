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
                 return render_template("warning.html", message="El usuario ya existe")
            
            UsersLooged.append(username)

            session['username'] = username

            #Recordamos el inicio de sesion
            session.permanent = True

            return redirect("/channels/Public")
    else:
            return render_template("inicio.html")

@app.route("/modificacion", methods=['GET', 'POST'])
@login_required
def modificacion(): 
    message = ""
    username = request.form.get("username")

    try:
          UsersLooged.remove(session['username'])
    except ValueError:
          pass
    if request.method == "POST":
          
          if username in UsersLooged:
                return render_template("warning.html", message="Usuario ya existe")
          UsersLooged.append(username)
          
          session['username'] == username

          return redirect("/channels/Public")
    else:
          return render_template("modificacion.html", channels=channelsCreated)
    
@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
      try:
            UsersLooged.remove(session['username'])
      except ValueError:
            pass
      return redirect("/inicio")

@app.route("/crear", methods=['GET', 'POST'])
@login_required
def crear():
      newChannel = request.form.get("channel")
      if request.method == "POST":
            if newChannel in channelsCreated:
                  return render_template("warning.html", message="Este canal ya Existe", channels=channelsCreated)
            channelsMessages[newChannel] = deque()

            return redirect("/channels/" +newChannel)
      else:
            return render_template("create.html", channelsCreated)
      
@app.route("/channels/<string:channel>", methods=['GET', 'POST'])
@login_required
def enter_channel(channel):
    ''' Channel page '''

    user = session['username']

    # actualizar canal actual de usario
    session['current_channel'] = channel

    if channel not in channelsCreated:
        return redirect("/channels/Public")

    if request.method == "POST":

        return redirect("/")
    else:
        return render_template("channel.html", channels=channelsCreated, messages=channelsMessages[channel], usersLogged=UsersLooged, user=user)


@socketio.on("joined")
def joined():
    ''' Announce user has entered to the channel '''

    room = session.get('current_channel')

    join_room(room)

    emit('status', {
        'userJoined': session.get('username'),
        'channel': room,
        'msg': str(session.get('username')) + ' se ha unido al canal.'},
        room=room)


@socketio.on('send message')
def send_msg(msg, timestamp):
    ''' Put the message in the channel '''

    # Enviar solo a usuarios en el mismo canal
    room = session.get('current_channel')

    # Guardar sms
    channelsMessages[room].append([timestamp, session.get('username'), msg])

    emit('announce message', {
        'user': session.get('username'),
        'timestamp': timestamp,
        'msg': msg},
        room=room)


@socketio.on("exit")
def exit():
    ''' Announce user has left the channel '''
    print("Recent Signal")

    room = session.get('current_channel')

    leave_room(room)

    emit('status', {
        'msg': str(session.get('username')) + ' ha abandonado el canal'},
        room=room)


if __name__ == "__main__":
    socketio.run(app)

      

