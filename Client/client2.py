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


@sio.event
def connect():
    print("I'm connected!")

    # p = int(input("Testing emit enter number greater than 0 "))
    # if p > 0:
    #     sio.emit('input', {'number': p})
gdata = None


@sio.on('begin')
def beginGame(data):
    global gdata
    gdata = data


def main():
    """ Main Program """

    # Call this function so the Pygame library can initialize itself
    pygame.init()

    # Create an 800x600 sized screen
    screen = pygame.display.set_mode([800, 600])

    # Set the title of the window
    pygame.display.set_caption('Maze Runner')

    # Create the player paddle object
    player = Player(50, 50, WHITE)

    # Creating Danner
    danner = Player(100, 100, RED)
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(5, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, -5)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, 5)

                if event.key == pygame.K_a:
                    danner.changespeed(-5, 0)
                if event.key == pygame.K_d:
                    danner.changespeed(5, 0)
                if event.key == pygame.K_w:
                    danner.changespeed(0, -5)
                if event.key == pygame.K_s:
                    danner.changespeed(0, 5)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(5, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, 5)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, -5)

                if event.key == pygame.K_a:
                    danner.changespeed(5, 0)
                if event.key == pygame.K_d:
                    danner.changespeed(-5, 0)
                if event.key == pygame.K_w:
                    danner.changespeed(0, 5)
                if event.key == pygame.K_s:
                    danner.changespeed(0, -5)

        # --- Game Logic ---

        player.move_player(current_room.wall_list, danner)

        danner.move_danner(current_room.wall_list, player)

        sio.emit("nextkey", {"Player": [
            player.rect.x, player.rect.y], "Danner": None, "frameNo": frameNo})
        screen.fill(BLACK)
        if gdata != None and frameNo-gdata["frameNo"] > 7:
            player.set_position(gdata["Player"])
        movingsprites.draw(screen)
        current_room.wall_list.draw(screen)

        pygame.display.flip()
        clock.tick(30)
        frameNo = (frameNo+1) % 10000000001
    pygame.quit()


if __name__ == "__main__":
    # sio.connect('http://0.0.0.0:5004')
    sio.connect("https://socket-game-project.herokuapp.com/")
    main()
