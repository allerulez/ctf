import pygame
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]


#pack_file = os.path.join(main_dir, 'data', pack_file)
pack_file = open('data/pack_file.txt')
pack = pack_file.read()
pack_file.close()

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

"""
def load_pack(pack, tile):
    " String -> change scheme"
    if pack == "potato" or pack == "standard":

        # Image of a missile
        if tile == "missile":
        missile = load_image(str(pack)+'/' + str(tile) + '.png')


        elif tile == "grass":
        # Image of a grass tile
        grass     = load_image(str(pack)+'/' + str(tile) + '.png')

        # Image of a rock box (str(pack)+w/all)
        rockbox   = load_image(str(pack)+'/' + str(tile) + '.png')

        # Image of a metal box
        metalbox  = load_image(str(pack)+'/' + str(tile) + '.png')

        # Image of a wood box
        woodbox   = load_image(str(pack)+'/' + str(tile) + '.png')

        # Image of a portal
        portal    = load_image(str(pack)+'/' + str(tile) + '.png')

        #Images of tanks
        tanks     = [load_image(str(pack)+'/' + str(tile) + '.png'), load_image(str(pack)+'/' + str(tile) + '.png'), load_image(str(pack)+'/' + str(tile) + '.png'),
             load_image(str(pack)+'/' + str(tile) + '.png'), load_image(str(pack)+'/' + str(tile) + '.png'),  load_image(str(pack)+'/' + str(tile) + '.png')]
    else:
        load_pack("standard")
"""
# Define the window's scale
IM_SCALE = 2

# Define the default size of tiles

TILE_SIZE = 40*IM_SCALE
"""
missile = load_pack(pack, "missile")
grass = load_pack(pack, "grass")
rockbox = load_pack(pack, "rockbox")
metalbox = load_pack(pack, "metalbox")
woodbox = load_pack(pack, "woodbox")
portal = load_pack(pack, "portal")

def get_missile(pack):

    return load_image(str(pack)+'/missile.png')
"""


missile = load_image(str(pack)+'/missile.png')
#def get_grass(pack):
grass = load_image(str(pack)+'/grass.png')

rockbox = load_image(str(pack)+'/rockbox.png')

metalbox = load_image(str(pack)+'/metalbox.png')

woodbox = load_image(str(pack)+'/woodbox.png')

portal = load_image(str(pack)+'/portal.png')

tanks     = [load_image(str(pack)+'/tank_orange.png'), load_image(str(pack)+'/tank_blue.png'), load_image(str(pack)+'/tank_white.png'),
             load_image(str(pack)+'/tank_yellow.png'), load_image(str(pack)+'/tank_red.png'),  load_image(str(pack)+'/tank_gray.png')]


sticky_missile = load_image('standard/sticky_missile.png')
# Image of overheat
overheat = load_image('overheat.png')

# Image of an explosion
explosion = load_image('explosion.png')

# Image of a small explosion
small_explosion = load_image('small_explosion.png')

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

died_to_oh = [load_image('kills/player1_died_to_oh.png'), load_image('kills/player2_died_to_oh.png')]
# List of image of tanks of different colors


# List of image of bases corresponding to the color of each tank
bases     = [load_image('base_orange.png'), load_image('base_blue.png'), load_image('base_white.png'),
             load_image('base_yellow.png'), load_image('base_red.png'),  load_image('base_gray.png')]
