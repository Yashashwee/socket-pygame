from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
sio = SocketIO(app)


@sio.event
def connect(sid):
    print("connedted ", sid)


@sio.on('message')
def print_message(sid, message):
    print(sid, " ", message)


@sio.on('input')
def print_number(sid, num):
    sio.emit('begin', {"gameData": "dummy"})


@sio.on('nextkey')
def nextKey(key):
    print(key)
    sio.emit('begin', key)


@app.route("/")
def index():
    return "Connected"


if __name__ == '__main__':
    sio.run(app)
