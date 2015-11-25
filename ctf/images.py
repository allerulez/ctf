import pygame
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]

#
# Load an image from the data directory
#
def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert_alpha()


# Define the window's scale
IM_SCALE = 2

# Define the default size of tiles
TILE_SIZE = 40*IM_SCALE


# Image of a missile
missile = load_image('missile.png')

# Image of an explosion
explosion = load_image('explosion.png')

# Image of a small explosion
small_explosion = load_image('small_explosion.png')

# Image of overheat
overheat = load_image('overheat.png')

# Image of deathtext 1
player1_dead = load_image('kills/player1_died_to_oh.png')

# Image of a grass tile
grass     = load_image('grass.png')

# Image of a rock box (wall)
rockbox   = load_image('rockbox.png')

# Image of a metal box
metalbox  = load_image('metalbox.png')

# Image of a wood box
woodbox   = load_image('woodbox.png')

# Image of a portal
portal	  = load_image('portal.png')

# Image of flag
flag      = load_image('flag.png')

# Image of health points (hearts)
hp		  = load_image('hp.png')

#Image of pause
pause	  = load_image('pause.png')

#Image of spawn protection
spawn_protect = load_image('spawn_protect.png')

#Image of overlay
overlay	  = load_image('overlay.png')

# Image of Tab
tab = load_image('overlay/overlay.png')

was_killed = [load_image('kills/player1_was_killed.png'), load_image('kills/player2_was_killed.png'), load_image('kills/player3_was_killed.png'),
			 load_image('kills/player4_was_killed.png'), load_image('kills/player5_was_killed.png'), load_image('kills/player6_was_killed.png')]


# List of image of tanks of different colors
tanks     = [load_image('tank_orange.png'), load_image('tank_blue.png'), load_image('tank_white.png'),
             load_image('tank_yellow.png'), load_image('tank_red.png'),  load_image('tank_gray.png')]

# List of image of bases corresponding to the color of each tank
bases     = [load_image('base_orange.png'), load_image('base_blue.png'), load_image('base_white.png'),
             load_image('base_yellow.png'), load_image('base_red.png'),  load_image('base_gray.png')]
