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
socketio = SocketIO(app)


@app.route('/')
def index():
    return "Hello"


@socketio.on("message")
def handleMessage(data):
    """
    :parameter: data
    """
    emit("new_message", data, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)
