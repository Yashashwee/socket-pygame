from flask import Flask, render_template, make_response, redirect
from flask_socketio import SocketIO, send, emit
import os

app = Flask(__name__)
sio = SocketIO(app)


@app.route('/')
def index():
    return "Hello"


@sio.on('message')
def print_message(message):
    print(message)


@sio.on('input')
def print_number(sid, num):
    sio.emit('begin', None)


@sio.on('nextkey')
def nextKey(key):
    print(key)
    sio.emit('begin', key)


if __name__ == '__main__':
    sio.run(app, debug=True, host='0.0.0.0', port=5004)
