import pygame
import sys
from rgb import PURPLE, BLACK, BLUE, RED, WHITE, GREEN

# Background Image
BACKGROUND_IMG = pygame.image.load("gameover.jpg")
BACKGROUND_IMG2 = pygame.image.load("gamewin.jpg")


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

    def changespeed(self, x, y):
        """ Change the speed of the player. Called with a keypress. """
        self.change_x += x
        self.change_y += y

    def set_position(self, Coord=None):
        if Coord != None or len(Coord) != 0:
            self.rect.x = Coord[0]
            self.rect.y = Coord[1]

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
