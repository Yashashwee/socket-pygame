import sys
import pygame
from aiohttp import web
import socketio


sio = socketio.AsyncServer()
app = web.Application()

sio.attach(app)


async def index(req):
    return "hello"


@sio.on('message')
async def print_message(sid, message):
    print(sid, " ", message)


@sio.on('input')
async def print_number(sid, num):
    await sio.emit('begin', {"gameData": "dummy"})


@sio.on('nextkey')
async def nextKey(sid, key):
    print(key)

    await sio.emit('begin', {"gameData": key}, to=sid)

app.router.add_get('/', index)


if __name__ == "__main__":
    web.run_app(app)
    # main()
