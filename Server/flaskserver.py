import collections
try:
    from collections import abc
    collections.MutableMapping = abc.MutableMapping
except:
    pass
from flask import Flask, render_template, make_response, redirect
from flask_socketio import SocketIO, send, emit
import os
import time

app = Flask(__name__)
sio = SocketIO(app)


def checkOverlap(player, danner):
    """
    | checking the overlap of player and danner
    | parameter 1: player coordinates
    | parameter 2: danner coordinates
    """
    l1 = player
    r1 = [l1[0]+15, l1[1]-15]
    l2 = danner

    r2 = [l2[0]+15, l2[1]-15]
    # If one rectangle is on left side of other
    if l1[0] > r2[0] or l2[0] > r1[0]:
        return False

    # If one rectangle is above other
    if r1[1] > l2[1] or r2[1] > l1[1]:
        return False

    return True


# initializing initial state
players = []
gdata = {"Player": [50, 50], "Danner": [
    100, 100], "frameNo": [0, 0], "winner": None}
frames = [0, 0]

# sio.emit('begin', gdata)


@app.route('/')
def index():
    return "Hello"


@sio.on('testoverlap')
def testOverlap(Coords):
    """
    | Test the overlap logic
    | param1: Coords ->  a tuple of player and danner coordinates
    """
    player = Coords[0]
    danner = Coords[1]
    return checkOverlap(player, danner)


@sio.on('resetPlayers')
def reset():
    """

    | Reset game state
    """
    global players
    global gdata
    players = []
    gdata = {"Player": [50, 50], "Danner": [
        100, 100], "frameNo": 0, "winner": None}
    return "RESET!!!"


@sio.on('user')
def choice(data):
    """
    | for the choice selection of user of player and danner
    | parameter: {"user":<name of user>,"choice":<0 or 1>}
    """
    global players
    global gdata
    # print(data)
    # print(players)
    if len(players) == 0:
        data["choice"] = data["choice"] % 2
        players.append(data)
        print(data)
        sio.emit("userresp", data)
    else:
        # if players[0]["choice"] == data["choice"]:
        data["choice"] = (players[0]["choice"]+1) % 2
        players.append(data)
        sio.emit("userresp", data)
        # else:
        #     data["choice"] = data["choice"] % 2
        #     players.append(data)
        #     sio.emit("userresp", data)
    sio.emit("begin", gdata)
    return gdata, data


@sio.on('message')
def print_message(message):
    """
    |Pass message to server for debuging
    :parameter: message
    """
    print(message)
    return message


@sio.on('input')
def print_number(sid, num):
    """
    Pass client info and unique num
    :parameter 1: sid
    :parameter 2: num
    """
    sio.emit('begin', None)
    return sid


@sio.on('nextkey')
def nextKey(data):
    """
    | next key
    | parameter: data={"Player/Danner":<coords>,"frameNo":<currentFrame>}.
    """
    global gdata
    global frames
    # gdata["frameNo"] = data["frameNo"]
    if data["Player"] == None:
        gdata["Danner"] = data["Danner"]
        frames[1] = data["frameNo"]
    else:
        gdata["Player"] = data["Player"]
        frames[0] = data["frameNo"]
    if(checkOverlap(gdata["Player"], gdata["Danner"])):
        gdata["winner"] = 1
    if(gdata["Player"][0] > 801):
        gdata["winner"] = 0
    gdata["frameNo"] = frames
    # time.sleep(data["delay"]/1000)
    sio.emit('begin', gdata)
    return gdata


@sio.event
def disconnect():
    """
    logic for disconnect
    """
    global players
    players = []
    gdata = {"Player": [50, 50], "Danner": [
        100, 100], "frameNo": 0, "winner": None}
    sio.emit("error", "Other player diconneted")


@sio.on('terminate')
def terminate(sid):
    """
    Closing connection
    """
    print(sid)
    sio.close_room(sid)


if __name__ == '__main__':
    sio.run(app, debug=True, host='0.0.0.0', port=5004)
