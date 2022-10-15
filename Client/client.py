import math
import time
import collections
import random
try:
    from collections import abc
    collections.MutableMapping = abc.MutableMapping
except:
    pass
import pygame
import platform
import sys
import os
import socketio
import pygame

if platform.system() == 'Linux':
    fileSystemGoBack = '.'
else:
    fileSystemGoBack = '..'
sys.path.insert(0, os.path.join(fileSystemGoBack, 'Game'))
from rgb import WHITE, RED, BLACK
from room import Room1
from players import Player

sys.path.insert(0, os.path.join(fileSystemGoBack, 'NetCode'))
from predict import *
#import asyncio

sio = socketio.Client()
setDelay = 0
frameDiff = 3
player = Player(50, 50, WHITE)
danner = Player(100, 100, RED)

roleChoice = {0: player, 1: danner}

temp = None


@sio.event
def connect():
    """
    connection establishment 
    """
    global temp
    temp = "I'm connected!"
    print(temp)


    # p = int(input("Testing emit enter number greater than 0 "))
    # if p > 0:
    #     sio.emit('input', {'number': p})
gdata = None
user = None


@sio.on('begin')
def beginGame(data):
    """
    | starting game 
    | parameter: data
    """
    global gdata
    if setDelay != 0:
        time.sleep(setDelay/1000)
    gdata = data


@sio.on('error')
def error(msg):
    """
    | error logic
    | parameter: msg
    """
    print(msg)
    global player
    global danner
    sio.emit("terminate", sio.sid)
    player.show_go_screen()
    # pygame.quit()
    time.sleep(2)
    os._exit(1)


@sio.on('userresp')
def resp(data):
    """
    :parameter: data
    """
    global user
    print(data)
    if user != None and data["name"] == user["name"]:
        user = data


def main():
    """ 
    Main Program for the game
    """
    global user
    pname = input("Enter player name ")
    choice = int(input("Enter 0 for player 1 for danner "))
    user = {"name": pname, "choice": choice}
    sio.emit("user", user)

    # Call this function so the Pygame library can initialize itself
    pygame.init()

    # Create an 800x600 sized screen
    screen = pygame.display.set_mode([800, 600])

    # Set the title of the window
    pygame.display.set_caption(pname)

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
                os._exit(1)
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
        if random.random() <= 0.25:
            sio.sleep(setDelay/1000)
        if user["choice"] == 0:

            danner.set_position(gdata["Danner"], current_room.wall_list)
            sio.emit("nextkey", {"Player": [
                player.rect.x, player.rect.y], "Danner": None, "frameNo": frameNo, "winner": None, "delay": setDelay})
        else:
            player.set_position(gdata["Player"], current_room.wall_list)
            sio.emit("nextkey", {"Player": None, "Danner": [
                     danner.rect.x, danner.rect.y], "frameNo": frameNo, "winner": None, "delay": setDelay})
        screen.fill(BLACK)
        if gdata != None:
            if gdata["winner"] != None:
                print(gdata["winner"])
                if user["choice"] == gdata["winner"]:
                    roleChoice[gdata["winner"]].show_win_screen()
                else:
                    roleChoice[user["choice"]].show_go_screen()

            # if frameNo-gdata["frameNo"][user["choice"]] > frameDiff:
            #     if user["choice"] == 0:
            #         player.set_position(gdata["Player"])
            #     else:
            #         danner.set_position(gdata["Danner"])
            #     frameNo = gdata["frameNo"][user["choice"]]
            # print("Self frame = ",frameNo-gdata["frameNo"][user["choice"]])
            # print("different frame = ",frameNo-gdata["frameNo"][(user["choice"]+1)%2])

            if frameNo-gdata["frameNo"][user["choice"]] > frameDiff:
                if(user["choice"] == 0):
                    # prediction logic for danner
                    danner.set_position(predict_player_pos(
                        [danner.rect.x, danner.rect.y], [player.rect.x, player.rect.y], 1), current_room.wall_list)
                else:
                    # Prediction logic for player
                    player.set_position(predict_player_pos(
                        [player.rect.x, player.rect.y], [danner.rect.x, danner.rect.y], 0), current_room.wall_list)

            if frameNo-gdata["frameNo"][user["choice"]] <= frameDiff:
                # print("ROLLBACK FOLKS!!")
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
                # frameNo = gdata["frameNo"][user["choice"]]

        movingsprites.draw(screen)
        current_room.wall_list.draw(screen)

        pygame.display.flip()
        clock.tick(30)
        frameNo = (frameNo+1) % 10000000001
    pygame.quit()


if __name__ == "__main__":
    if (len(sys.argv)) > 1:
        setDelay = int(sys.argv[1])
    sio.connect('http://10.194.33.76:5004')
    # sio.connect("https://socket-game-project.herokuapp.com/")
    main()
