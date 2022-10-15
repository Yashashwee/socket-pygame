import math
import time
import collections
try:
    from collections import abc
    collections.MutableMapping = abc.MutableMapping
except:
    pass
import pygame
import sys
import os
from players import Player
from room import Room1
from rgb import WHITE, RED, BLACK
import socketio
import pygame
from predict import predict_player_pos
import asyncio

sio = socketio.AsyncClient()
setDelay = 0
frameDiff = 0
player = Player(50, 50, WHITE)
danner = Player(100, 100, RED)

roleChoice = {0: player, 1: danner}

temp = None


@sio.event
def connect():
    global temp
    temp = "I'm connected!"
    print(temp)

    # p = int(input("Testing emit enter number greater than 0 "))
    # if p > 0:
    #     sio.emit('input', {'number': p})
gdata = None
user = None


@sio.on('begin')
async def beginGame(data):
    """
    :parameter: data
    """
    global gdata
    await sio.sleep(setDelay/1000)
    gdata = data


@sio.on('error')
async def error(msg):
    """
    :parameter: msg
    """
    print(msg)
    global player
    global danner
    await sio.emit("terminate", sio.sid)
    player.show_go_screen()
    # pygame.quit()
    time.sleep(2)
    os._exit(1)


@sio.on('userresp')
async def resp(data):
    """
    :parameter: data
    """
    global user
    if user != None and data["name"] == user["name"]:
        user = data


async def main():
    """ Main Program """
    global user
    await sio.connect('http://0.0.0.0:5004')
    pname = input("Enter player name ")
    choice = int(input("Enter 0 for player 1 for danner "))
    user = {"name": pname, "choice": choice}
    await sio.emit("user", user)

    # Call this function so the Pygame library can initialize itself
    pygame.init()

    # Create an 800x600 sized screen
    screen = pygame.display.set_mode([800, 600])

    # Set the title of the window
    pygame.display.set_caption('Pakdam Pakdai')

    # Create the player paddle object
    global player
    # Creating Danner
    global danner
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)
    movingsprites.add(danner)

    current_room = Room1()
    clock = pygame.time.Clock()

    done = False
    frameNo = 0
    while not done:

        # --- Event Processing ---

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if user["choice"] == 0:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.changespeed(-5, 0)
                    if event.key == pygame.K_RIGHT:
                        player.changespeed(5, 0)
                    if event.key == pygame.K_UP:
                        player.changespeed(0, -5)
                    if event.key == pygame.K_DOWN:
                        player.changespeed(0, 5)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.changespeed(5, 0)
                    if event.key == pygame.K_RIGHT:
                        player.changespeed(-5, 0)
                    if event.key == pygame.K_UP:
                        player.changespeed(0, 5)
                    if event.key == pygame.K_DOWN:
                        player.changespeed(0, -5)
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        danner.changespeed(-5, 0)
                    if event.key == pygame.K_RIGHT:
                        danner.changespeed(5, 0)
                    if event.key == pygame.K_UP:
                        danner.changespeed(0, -5)
                    if event.key == pygame.K_DOWN:
                        danner.changespeed(0, 5)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        danner.changespeed(5, 0)
                    if event.key == pygame.K_RIGHT:
                        danner.changespeed(-5, 0)
                    if event.key == pygame.K_UP:
                        danner.changespeed(0, 5)
                    if event.key == pygame.K_DOWN:
                        danner.changespeed(0, -5)

        # --- Game Logic ---
        # print(current_room.wall_list)
        player.move_player(current_room.wall_list, danner)

        danner.move_danner(current_room.wall_list, player)
        await sio.sleep(setDelay/1000)
        if user["choice"] == 0:

            danner.set_position(gdata["Danner"], current_room.wall_list)
            await sio.emit("nextkey", {"Player": [
                player.rect.x, player.rect.y], "Danner": None, "frameNo": frameNo, "winner": None, "delay": setDelay})
        else:
            player.set_position(gdata["Player"], current_room.wall_list)
            await sio.emit("nextkey", {"Player": None, "Danner": [
                danner.rect.x, danner.rect.y], "frameNo": frameNo, "winner": None, "delay": setDelay})
        screen.fill(BLACK)
        if gdata != None:
            if gdata["winner"] != None:
                print(gdata["winner"])
                if user["choice"] == gdata["winner"]:
                    roleChoice[gdata["winner"]].show_win_screen()
                else:
                    roleChoice[user["choice"]].show_go_screen()

            # if frameNo-gdata["frameNo"] > frameDiff:
            #     if user["choice"] == 0:
            #         player.set_position(gdata["Player"])
            #     else:
            #         danner.set_position(gdata["Danner"])
            #     frameNo = gdata["frameNo"]

            if frameNo-gdata["frameNo"] > frameDiff:
                if(user["choice"] == 0):
                    # prediction logic for danner
                    danner.set_position(predict_player_pos(
                        [danner.rect.x, danner.rect.y], [player.rect.x, player.rect.y], 1), current_room.wall_list)
                else:
                    # Prediction logic for player
                    player.set_position(predict_player_pos(
                        [player.rect.x, player.rect.y], [danner.rect.x, danner.rect.y], 0), current_room.wall_list)

            if frameNo-gdata["frameNo"] <= frameDiff:
                if user["choice"] == 0:
                    # Rollback:
                    if(player.rect.x != gdata["Player"][0] and player.rect.y != gdata["Player"][1]):
                        player.set_position(
                            gdata["Player"], current_room.wall_list)
                else:
                    # Rollback
                    if(danner.rect.x != gdata["Danner"][0] and danner.rect.y != gdata["Danner"][1]):
                        danner.set_position(
                            gdata["Danner"], current_room.wall_list)
                frameNo = gdata["frameNo"]

        movingsprites.draw(screen)
        current_room.wall_list.draw(screen)

        pygame.display.flip()
        clock.tick(30)
        frameNo = (frameNo+1) % 10000000001
    pygame.quit()


if __name__ == "__main__":
    if (len(sys.argv)) > 1:
        setDelay = int(sys.argv[1])
    # sio.connect('http://0.0.0.0:5004')
    # sio.connect("https://socket-game-project.herokuapp.com/")
    asyncio.run(main())
