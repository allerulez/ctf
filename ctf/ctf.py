import pygame
from pygame.locals import *
from pygame.color import *
import pymunk as pm

#----- Initialisation -----#

#-- Initialise the display
pygame.init()
pygame.display.set_mode()

#-- Initialise the clock
clock = pygame.time.Clock()

#-- Initialise the physics engine
space = pm.Space()
space.gravity = (0.0,  0.0)

#-- Import from the ctf framework
import ai
import boxmodels
import images
import gameobjects
import maps

#-- Constants
framerate = 60

#-- Variables
#   Define the current level
current_map         = maps.map0
#   List of all game objects
game_objects_list   = []
tanks_list          = []

#-- Resize the screen to the size of the current level
screen = pygame.display.set_mode(current_map.rect().size)

#<INSERT GENERATE BACKGROUND>

background = pygame.Surface(screen.get_size())
#   Copy the grass tile all over the level area
#   The map has dimension a width of "current_map.width" and a height of "current_map.height"
#   The first loop will iterate "x" between "0" and "width-1" and the second loop will iterate
#   "y" between "0" and "height-1"
#""
for x in range(0, current_map.width):
    for y in range(0, current_map.height):
    	# The call to the function "blit" will copy the image contained in "images.grass"
    	# into the "background" image at the coordinates given as the secnod argument
        background.blit(images.grass, (x*images.TILE_SIZE, y*images.TILE_SIZE))

#<INSERT CREATE BOXES>
#   The initial position and type of the boxes is contained in the "current_map.boxes" array,
#   which is an array that has the size of the map, and whose cells contain the box type
#   (0 means no box, 1 means wall, 2 means wood and 3 means steel)
#
#   As for the background we create two loops over the size of the map.
#
for x in range(0, current_map.width):
	for y in range(0, current_map.height):
		# Get the type of boxes fo the current cell(y, x)
		box_type = current_map.boxAt(x, y)
		# We need to get the python object that corresponds to the model
		box_model = boxmodels.get_model(box_type)
		# If the box model is non nyll, create a box
		if(box_model != None):
			# Create a "Box" using the model "box_model" at the coordinate (x,y) 
			# (an offset of 0.5 is added since the constructor of the Box object expects to 
			#  know the centre of the box, have a look at the coordinate system section for 
			#  further explanation)
			box = gameobjects.Box(x + 0.5, y + 0.5, box_model, space)
			game_objects_list.append(box)



#<INSERT CREATE TANKS>

#<INSERT CREATE FLAG>

#----- Main Loop -----#

#-- Control whether the game run
running = True

skip_update = 0

while running:
    #-- Handle the events
    for event in pygame.event.get():
        # Check if we receive a QUIT event (for instance, if the user press the
        # close button of the wiendow) or if the user press the escape key.
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
    #-- Update physics
    if(skip_update == 0):
      # Loop over all the game objects and update their speed in function of their
      # acceleration.
      for obj in game_objects_list:
        obj.update()
      skip_update = 5
    else:
      skip_update -= 1
    
    #   Check collisions and update the objects position
    space.step(1 / framerate)

    #   Update object that depends on an other object position (for instance a flag)
    for obj in game_objects_list:
      obj.post_update()
    #-- Update Display
    
    #<INSERT DISPLAY BACKGROUND>
    # Display the background on the screen
    screen.blit(background,(0,0))
    
    #<INSERT DISPLAY OBJECTS>
    # Update the game display of the game objects on the screen
    for obj in game_objects_list:
    	# For each object, simply call the "update_screen" function
    	obj.update_screen(screen)
    


    #   Redisplay the entire screen (see double buffer technique)
    pygame.display.flip()

    #   Control the game framerate
    clock.tick(framerate)
#get default_pos(brick):
# Det ska ge ut def positionen på ett objekt