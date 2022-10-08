from flask import Flask, render_template, make_response, redirect
from flask_socketio import SocketIO, send, emit
import os

app = Flask(__name__)
sio = SocketIO(app)

players = []
gdata = {"Player": [50, 50], "Danner": [
    100, 100], "frameNo": 0, "winner": None}


@app.route('/')
def index():
    return "Hello"


@sio.on('user')
def choice(data):
    global players
    global gdata
    # print(data)
    # print(players)
    if len(players) == 0:
        players.append(data)
        print(data)
        sio.emit("userresp", data)
    else:
        if players[0]["choice"] == data["choice"]:
            data["choice"] = (players[0]["choice"]+1) % 2
            sio.emit("userresp", data)
        else:
            sio.emit("userresp", data)
    sio.emit("begin", gdata)
    # print(data)


@sio.on('message')
def print_message(message):
    print(message)


@sio.on('input')
def print_number(sid, num):
    sio.emit('begin', None)


@sio.on('nextkey')
def nextKey(data):
    global gdata
    gdata["frameNo"] = data["frameNo"]
    if data["Player"] == None:
        gdata["Danner"] = data["Danner"]
    else:
        gdata["Player"] = data["Player"]
    sio.emit('begin', gdata)


if __name__ == '__main__':
    sio.run(app, debug=True, host='0.0.0.0', port=5004)
