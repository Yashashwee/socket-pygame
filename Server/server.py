import collections
try:
    from collections import abc
    collections.MutableMapping = abc.MutableMapping
except:
    pass
import sys
import pygame
from aiohttp import web
import socketio


sio = socketio.AsyncServer()
app = web.Application()

sio.attach(app)


async def index(req):
    """
    :parameter: req
    """
    return "hello"


@sio.on('message')
async def print_message(sid, message):
    """
    :parameter1: sid
    :parameter2: message
    """
    print(sid, " ", message)


@sio.on('input')
async def print_number(sid, num):
    """
    :parameter1: sid
    :parameter2: num
    """
    await sio.emit('begin', {"gameData": "dummy"})


@sio.on('nextkey')
async def nextKey(sid, key):
    """
    :parameter1: sid
    :parameter2: key
    """
    print(key)

    await sio.emit('begin', {sid: key})

app.router.add_get('/', index)


if __name__ == "__main__":
    web.run_app(app)
    # main()
