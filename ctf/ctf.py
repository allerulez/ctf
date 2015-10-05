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
game_objects_def_pos_list = []
tanks_list          = []

#-- Resize the screen to the size of the current level
screen = pygame.display.set_mode(current_map.rect().size)



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
game_objects_def_pos_list = list(game_objects_list)

def default_pos(tile):
#	x = game_objects_def_pos_list[tile][0]
#	y = game_objects_def_pos_list[tile][1]
	return tile in game_objects_def_pos_list


# Create the tanks
# Loop over the starting position

for i in range(0, len(current_map.start_positions)):
	# Get the starting position of the tank "i"
	pos = current_map.start_positions[i]
	# Create the tank, images.tank contains the image
	tank = gameobjects.Tank(pos[0], pos[1], pos[2], images.tanks[i], space)
	# Add the tank to the list of objects to display
	game_objects_list.append(tank)
	# Add the tank to the list of tanks
	tanks_list.append(tank)



# This function call create a new flag object at coordinates x, y
flag = gameobjects.Flag(current_map.width/2, current_map.height/2)
game_objects_list.append(flag)

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
		if event.type == KEYDOWN and event.key == K_UP:
			gameobjects.Tank.accelerate(tanks_list[0])
		elif event.type == KEYUP and event.key == K_UP:
			gameobjects.Tank.stop_moving(tanks_list[0])
		if event.type == KEYDOWN and event.key == K_DOWN:
			gameobjects.Tank.decelerate(tanks_list[0])
		elif event.type == KEYUP and event.key == K_DOWN:
			gameobjects.Tank.stop_moving(tanks_list[0])
		if event.type == KEYDOWN and event.key == K_LEFT:
			gameobjects.Tank.turn_left(tanks_list[0])
		elif event.type == KEYUP and event.key == K_LEFT:
			gameobjects.Tank.stop_turning(tanks_list[0])
		if event.type == KEYDOWN and event.key == K_RIGHT:
			gameobjects.Tank.turn_right(tanks_list[0])
		elif event.type == KEYUP and event.key == K_RIGHT:
			gameobjects.Tank.stop_turning(tanks_list[0])
		#gameobjects.Tank.stop_moving(tanks_list[0])

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
	

	# Display the background on the screen
	screen.blit(background,(0,0))
	

	# Update the game display of the game objects on the screen
	for obj in game_objects_list:
		# For each object, simply call the "update_screen" function
		if default_pos(obj) != obj:
			obj.update_screen(screen)
	



	#   Redisplay the entire screen (see double buffer technique)
	pygame.display.flip()

	#   Control the game framerate
	clock.tick(framerate)
