import collections
try:
    from collections import abc
    collections.MutableMapping = abc.MutableMapping
except:
    pass
import pygame
import sys
from players import Player
from room import Room1
from rgb import WHITE, RED, BLACK
import socketio
import pygame
import sys
#import asyncio

sio = socketio.Client()

frameDiff = 7
player = Player(50, 50, WHITE)
danner = Player(100, 100, RED)

roleChoice = {0: player, 1: danner}


@sio.event
def connect():
    print("I'm connected!")

    # p = int(input("Testing emit enter number greater than 0 "))
    # if p > 0:
    #     sio.emit('input', {'number': p})
gdata = None
user = None


@sio.on('begin')
def beginGame(data):
    """
    :parameter: data
    """
    global gdata
    gdata = data


@sio.on('error')
def error(msg):
    """
    :parameter: msg
    """
    print(msg)
    global player
    global danner
    sio.emit("terminate", sio.sid)
    player.show_go_screen()


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
    """ Main Program """
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
    pygame.display.set_caption('Maze Runner')

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

        player.move_player(current_room.wall_list, danner)

        danner.move_danner(current_room.wall_list, player)
        if user["choice"] == 0:
            danner.set_position(gdata["Danner"])
            sio.emit("nextkey", {"Player": [
                player.rect.x, player.rect.y], "Danner": None, "frameNo": frameNo, "winner": None})
        else:
            player.set_position(gdata["Player"])
            sio.emit("nextkey", {"Player": None, "Danner": [
                     danner.rect.x, danner.rect.y], "frameNo": frameNo, "winner": None})
        screen.fill(BLACK)
        if gdata != None:
            if gdata["winner"] != None:
                print(gdata["winner"])
                if user["choice"] == gdata["winner"]:
                    roleChoice[gdata["winner"]].show_win_screen()
                else:
                    roleChoice[user["choice"]].show_go_screen()
            if frameNo-gdata["frameNo"] > frameDiff:
                if user["choice"] == 0:
                    player.set_position(gdata["Player"])
                else:
                    danner.set_position(gdata["Danner"])
                frameNo = gdata["frameNo"]

        movingsprites.draw(screen)
        current_room.wall_list.draw(screen)

        pygame.display.flip()
        clock.tick(30)
        frameNo = (frameNo+1) % 10000000001
    pygame.quit()


if __name__ == "__main__":
    sio.connect('http://0.0.0.0:5004')
    # sio.connect("https://socket-game-project.herokuapp.com/")
    main()
