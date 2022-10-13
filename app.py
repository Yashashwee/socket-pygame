import collections
try:
    from collections import abc
    collections.MutableMapping = abc.MutableMapping
except:
    pass
from flask import Flask, render_template, make_response, redirect
from flask_socketio import SocketIO, send, emit
import os

app = Flask(__name__)
sio = SocketIO(app)


def checkOverlap(player, danner):
    l1 = player
    # r1 = [l1[0]+15, l1[1]-15]
    l2 = danner

    com_p_x = player[0] + 7.5
    com_p_y = player[1] + 7.5

    com_d_x = danner[0] + 7.5
    com_d_y = danner[1] + 7.5

    if(math.sqrt((com_p2_y-com_p1_y)**2 + (com_p2_x-com_p1_x)**2) <= 15):
        return True
    else:
        return False

    # r2 = [l2[0]+15, l2[1]-15]
    # # If one rectangle is on left side of other
    # if l1[0] > r2[0] or l2[0] > r1[0]:
    #     return False

    # # If one rectangle is above other
    # if r1[1] > l2[1] or r2[1] > l1[1]:
    #     return False

    # return True


players = []
gdata = {"Player": [50, 50], "Danner": [
    100, 100], "frameNo": 0, "winner": None}


@app.route('/')
def index():
    return "Hello"


@sio.on('user')
def choice(data):
    """
    :parameter: data
    """
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
    """
    :parameter: message
    """
    print(message)


@sio.on('input')
def print_number(sid, num):
    """
    :parameter 1: sid
    :parameter 2: num
    """
    sio.emit('begin', None)


@sio.on('nextkey')
def nextKey(data):
    """
    :parameter: data
    """
    global gdata
    gdata["frameNo"] = data["frameNo"]
    if data["Player"] == None:
        gdata["Danner"] = data["Danner"]
    else:
        gdata["Player"] = data["Player"]
    if(checkOverlap(gdata["Player"], gdata["Danner"])):
        gdata["winner"] = 1
    if(gdata["Player"][0] > 801):
        gdata["winner"] = 0
    sio.emit('begin', gdata)


@sio.event
def disconnect():
    global players
    sio.emit("error", "Other player diconneted")
    players = []
    gdata = {"Player": [50, 50], "Danner": [
        100, 100], "frameNo": 0, "winner": None}


@sio.on('terminate')
def terminate(sid):
    print(sid)
    sio.close_room(sid)


if __name__ == '__main__':
    sio.run(app, debug=True, host='0.0.0.0', port=5004)
