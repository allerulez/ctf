import pygame
import time	
import math
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
missile_list		= []
box_dict			= {}
exp_list			= []
exp_time			= []
tank_exp_list		= []
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

"""
base1 = gameobjects.GameVisibleObject(0.5, 0.5, images.bases[0])
base2 = gameobjects.GameVisibleObject(current_map.width - 0.5, 0.5, images.bases[1])
base3 = gameobjects.GameVisibleObject(0.5, current_map.height - 0.5, images.bases[2])
base4 = gameobjects.GameVisibleObject(current_map.width - 0.5, current_map.height - 0.5, images.bases[3])

game_objects_list.append(base1)
game_objects_list.append(base2)
game_objects_list.append(base3)
game_objects_list.append(base4)
"""

# --- Fence around the map START ---
nw_box = pm.Body()
se_box = pm.Body()
north_seg = pm.Segment(nw_box,  (-0.5, -0.5), (current_map.width + 0.5, -0.5), 0.5)
east_seg = pm.Segment(se_box, (current_map.width + 0.5, current_map.height + 0.5),(current_map.width + 0.5, -0.5), 0.5)
south_seg = pm.Segment(se_box,  (current_map.width + 0.5, current_map.height + 0.5),(-0.5 , current_map.height + 0.5), 0.5)
west_seg = pm.Segment(nw_box,   (-0.5, -0.5), (-0.5, current_map.height + 0.5), 0.5)
north_seg.collision_type = 10
east_seg.collision_type = 10
south_seg.collision_type = 10
west_seg.collision_type = 10
space.add(north_seg, east_seg, south_seg, west_seg)
# --- Fence around the map END ---


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
			if box_type == 2:
				box.shape.collision_type = 2
				box.hp = 1
			elif box_type == 1:				
				box.shape.collision_type = 10
			game_objects_list.append(box)
			box_dict[(x+0.5, y+0.5)] = box


game_objects_def_pos_list = list(game_objects_list)
ais = []
def default_pos(tile):
	return tile in game_objects_def_pos_list
# --- START ---
#def create_missile(tank):
#        x = GamePhysicsObject.screen_orientation(tank)
#        # SKAPA EN MISSIL
# --- END ---
"""
def tank_hit(missile, tank):
	mis_pos = gameobjects.GamePhysicsObject.screen_position(missile)
	tank_pos = gameobjects.GamePhysicsObject.screen_position(tank)
	if math.fabs(mis_pos[0]-tank_pos[0])< 30 and math.fabs(mis_pos[1]-tank_pos[1])< 30:
		return True
	return False

def box_hit(missile):
	pass


def missile_hit(missile):
	velo = math.sqrt(missile.body.velocity[0]**2 + missile.body.velocity[1]**2)
	if velo < 10.0:
		return True
	return False
"""
# This function call creates a new flag object at coordinates x, y
flag = gameobjects.Flag(current_map.width/2, current_map.height/2)
game_objects_list.append(flag)
# ---FIXA IMORGON ---
# Nya tiles
# Finare tiles
########### Visuell explosion: en liten explosion för missilen
########### samt en stor när en tank/låda sprängs.
# Visuell reload time, Överhettad tank / cirkel som snurrar
# Stållådorna ska få en högre friktion
# Stenlådorna ska få ett HP
# ---Mission COMPLETED ---

def tank_explosion(tank_or_box, image):
	tank_pos = tank_or_box.body.position
	exp = gameobjects.GameVisibleObject(tank_pos[0] , tank_pos[1], image)
	exp_list.append(exp)
	exp_start = time.time()
	exp_time.append(exp_start)
	game_objects_list.append(exp)
	def remove_explosion():
		if time.time() > exp_start + 0.5:
			exp_list.remove(exp)
			exp_time.remove(exp_start)
			game_objects_list.remove(exp)
			return True
		return False
	return remove_explosion


def tank_hit(space, arb):
	if arb.shapes[1].parent != tanks_list[0]:
		arb.shapes[1].parent.hp -= 1
		tank_exp_list.append(tank_explosion(arb.shapes[1].parent, images.small_explosion))
		if arb.shapes[1].parent.hp == 1:
			game_objects_list.remove(arb.shapes[1].parent.hp_vis[0])
		if arb.shapes[1].parent.hp == 0:
			if arb.shapes[1].parent.flag != None:
				flag_x = arb.shapes[1].parent.x_pos
				flag_y = arb.shapes[1].parent.y_pos
				arb.shapes[1].parent.flag = None
				arb.shapes[1].parent.body.position = arb.shapes[1].parent.start_position
				flag = gameobjects.Flag(flag_x, flag_y)	
			tank_exp_list.append(tank_explosion(arb.shapes[1].parent, images.explosion))
			arb.shapes[1].parent.hp = 2
			game_objects_list.append(arb.shapes[1].parent.hp_vis[0])
			arb.shapes[1].parent.body.position = arb.shapes[1].parent.start_position
		space.add_post_step_callback(space.remove, arb.shapes[0], arb.shapes[0].body)
		game_objects_list.remove(arb.shapes[0].parent)
	return 1 

def box_hit(space, arb):
	arb.shapes[1].parent.hp -= 1
	if arb.shapes[1].parent.hp == 0:
		tank_exp_list.append(tank_explosion(arb.shapes[1].parent, images.explosion))
		space.add_post_step_callback(space.remove, arb.shapes[1], arb.shapes[1].body)
		game_objects_list.remove(arb.shapes[1].parent)
	if arb.shapes[0].parent in game_objects_list:
		space.add_post_step_callback(space.remove, arb.shapes[0], arb.shapes[0].body)
		game_objects_list.remove(arb.shapes[0].parent)

	return 1


def other_hit(space, arb):
	
	if arb.shapes[0].parent in game_objects_list:
		space.add_post_step_callback(space.remove, arb.shapes[0], arb.shapes[0].body)
		game_objects_list.remove(arb.shapes[0].parent)
	return 1


# Create the tanks
# Loop over the starting position

for i in range(0, len(current_map.start_positions)):
	# Get the starting position of the tank "i"
	pos = current_map.start_positions[i]
	# Create the tank, images.tank contains the image
	tank = gameobjects.Tank(pos[0], pos[1], pos[2], images.tanks[i], space)
	# Add the tanks base to the map and game_objects_list
	base = gameobjects.GameVisibleObject(pos[0],pos[1], images.bases[i])
	# Add the tanks hp bar
	tank.hp_vis += [gameobjects.HP(pos[0]-0.2, pos[1]+0.25)]
	tank.hp_vis += [gameobjects.HP(pos[0]+0.2, pos[1]+0.25)]
	# Add the tank to the list of objects to display
	game_objects_list.append(tank)
	game_objects_list.append(base)
	"""
	tank.hp_vis += [hp1]
	tank.hp_vis += [hp2]
	"""
	for hp in tank.hp_vis:
		game_objects_list.append(hp)
		

	

	# Add the tank to the list of tanks
	tanks_list.append(tank)
	# Add the bases gameobjects

	#Add ai
	if i > 0:
		ais.append(ai.SimpleAi(tanks_list[i], game_objects_list, tanks_list, space))
	

# Collision handlers ----START----

space.add_collision_handler(0, 1, None, tank_hit)
space.add_collision_handler(0, 2, None, box_hit)
space.add_collision_handler(0, 10, None, other_hit)
# Collision handlers ----END----



#----- Main Loop -----#

#-- Control whether the game run
running = True
start = 0
exp_start = 0
skip_update = 0
	
while running:
	#-- Handle the events
	for event in pygame.event.get():
		# Check if we receive a QUIT event (for instance, if the user press the
		# close button of the window) or if the user press the escape key.
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
		if event.type == KEYDOWN and event.key == K_RETURN:
			if not start or time.time() > start + 2:

				m = gameobjects.Tank.shoot(tanks_list[0], space)
				missile_list.append(m)
				game_objects_list.append(m)
				start = time.time()
	
	if tank_exp_list and tank_exp_list[0]():
		tank_exp_list.pop(0)

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



	for i in range(len(tanks_list)):
                gameobjects.Tank.try_grab_flag(tanks_list[i], flag)
                if gameobjects.Tank.has_won(tanks_list[i]):
                        running = False
                if i < len(tanks_list)-1:
                        ai.SimpleAi.decide(ais[i])



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
