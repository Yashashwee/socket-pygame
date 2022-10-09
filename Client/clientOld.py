import collections
try:
    from collections import abc
    collections.MutableMapping = abc.MutableMapping
except:
    pass
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
gdata = [[50, 50], [100, 100]]


@sio.on('begin')
def beginGame(data):
    global gdata
    gdata = data


# asyncio.run(sio.connect('http://0.0.0.0:8080'))
# RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

# Background Image
BACKGROUND_IMG = pygame.image.load("gameover.jpg")
BACKGROUND_IMG2 = pygame.image.load("gamewin.jpg")


class Wall(pygame.sprite.Sprite):
    """This class represents the bar at the bottom that the player controls """

    def __init__(self, x, y, width, height, color):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Make a BLUE wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the
    player controls """

    # Checking whether player is player or danner
    player_color = WHITE
    # Set speed vector
    change_x = 0
    change_y = 0

    def __init__(self, x, y, color):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Get player info
        player_color = color

        # Set height, width
        self.image = pygame.Surface([15, 15])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def set_position(self, Coord=None):
        if Coord != None or len(Coord) != 0:
            self.rect.x = Coord[0]
            self.rect.y = Coord[1]

    def changespeed(self, x, y):
        """ Change the speed of the player. Called with a keypress. """
        self.change_x += 0.6*x
        self.change_y += 0.6*y

    def move_player(self, walls, player):
        """ Find a new position for the player """

        # Move left/right
        self.rect.x += self.change_x

        if(self.rect.x < 0):
            self.rect.x = 0

        if(self.rect.x > 801):
            self.show_win_screen()

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        if (pygame.sprite.collide_rect(self, player) == True):
            self.show_go_screen()

    def move_danner(self, walls, player):
        """ Find a new position for the player """

        # Move left/right
        self.rect.x += self.change_x

        if(self.rect.x < 0):
            self.rect.x = 0

        if(self.rect.x > 786):
            self.rect.x = 786

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        if (pygame.sprite.collide_rect(self, player) == True):
            self.show_go_screen()

    def show_go_screen(self):
        screen = pygame.display.set_mode([800, 600])
        screen.blit(BACKGROUND_IMG.convert(), (0, 0))

        FONT = pygame.font.Font('freesansbold.ttf', 32)
        text_surface = FONT.render(
            "Press space bar to play again", True, WHITE)
        screen.blit(text_surface, (100, 600 * 7 / 8))
        pygame.display.flip()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        done = True

            clock = pygame.time.Clock()
            clock.tick(60)
        sys.exit()

    def show_win_screen(self):
        screen = pygame.display.set_mode([800, 600])
        screen.blit(BACKGROUND_IMG2.convert(), (0, 0))

        FONT = pygame.font.Font('freesansbold.ttf', 32)
        text_surface = FONT.render(
            "Press space bar to play again", True, WHITE)
        screen.blit(text_surface, (100, 500))
        pygame.display.flip()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        done = True

            clock = pygame.time.Clock()
            clock.tick(60)
        sys.exit()


class Room(object):
    """ Base class for all rooms. """

    # Each room has a list of walls, and of enemy sprites.
    wall_list = None
    enemy_sprites = None

    def __init__(self):
        """ Constructor, create our lists. """
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()


class Room1(Room):
    """This creates all the walls in room 3"""

    def __init__(self):
        super().__init__()

        walls = [[0, 0, 20, 250, PURPLE],
                 [0, 350, 20, 250, PURPLE],
                 [780, 0, 20, 250, PURPLE],
                 [780, 350, 20, 250, PURPLE],
                 [20, 0, 760, 20, PURPLE],
                 [20, 580, 760, 20, PURPLE]
                 ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        for x in range(100, 800, 100):
            for y in range(50, 451, 300):
                wall = Wall(x, y, 20, 200, RED)
                self.wall_list.add(wall)

        for x in range(150, 700, 100):
            wall = Wall(x, 200, 20, 200, WHITE)
            self.wall_list.add(wall)


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

    while not done:

        # --- Event Processing ---

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # sio.emit("nextkey", pygame.K_LEFT)
                    player.changespeed(-5, 0)
                if event.key == pygame.K_RIGHT:
                    # sio.emit("nextkey", pygame.K_RIGHT)
                    player.changespeed(5, 0)
                if event.key == pygame.K_UP:
                    # sio.emit("nextkey", pygame.K_UP)
                    player.changespeed(0, -5)
                if event.key == pygame.K_DOWN:
                    # sio.emit("nextkey", pygame.K_DOWN)
                    player.changespeed(0, 5)

                if event.key == pygame.K_a:
                    # sio.emit("nextkey", [gdata[0],
                    #  [danner.rect.x, danner.rect.y]])
                    # print("nexKey")
                    danner.changespeed(-5, 0)
                if event.key == pygame.K_d:
                    # sio.emit("nextkey", [gdata[0],
                    #  [danner.rect.x, danner.rect.y]])
                    danner.changespeed(5, 0)
                    # print(danner.rect.x)
                if event.key == pygame.K_w:
                    # sio.emit("nextkey", [gdata[0],
                    #  [danner.rect.x, danner.rect.y]])
                    danner.changespeed(0, -5)
                if event.key == pygame.K_s:
                    # sio.emit("nextkey", [gdata[0],
                    #  [danner.rect.x, danner.rect.y]])
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
                    # sio.emit("nextkey", [gdata[0],
                    #  [danner.rect.x, danner.rect.y]])
                    danner.changespeed(5, 0)
                if event.key == pygame.K_d:
                    # sio.emit("nextkey", [gdata[0],
                    #  [danner.rect.x, danner.rect.y]])
                    danner.changespeed(-5, 0)
                if event.key == pygame.K_w:
                    # sio.emit("nextkey", [gdata[0],
                    #  [danner.rect.x, danner.rect.y]])
                    danner.changespeed(0, 5)
                if event.key == pygame.K_s:
                    # sio.emit("nextkey", [gdata[0],
                    #  [danner.rect.x, danner.rect.y]])
                    danner.changespeed(0, -5)

        # --- Game Logic ---

        player.move_player(current_room.wall_list, danner)

        danner.move_danner(current_room.wall_list, player)
        # print(danner.rect.x)
        sio.emit("nextkey", [gdata[0],
                             [danner.rect.x, danner.rect.y]])

        screen.fill(BLACK)

        movingsprites.draw(screen)
        current_room.wall_list.draw(screen)

        pygame.display.flip()
        if len(gdata) != 0:
            player.set_position(gdata[0])
            danner.set_position(gdata[1])

        clock.tick(20)

    pygame.quit()


if __name__ == "__main__":
    sio.connect('http://0.0.0.0:5004')
    # sio.connect("https://socket-game-project.herokuapp.com/")
    main()
