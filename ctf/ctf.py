import pygame
import time	
import math
import os
import argparse
import random
from pygame.locals import *
from pygame.color import *
import pymunk

#----- Initialisation -----#

#-- Initialise the display
pygame.init()
pygame.display.set_mode((600,800), RESIZABLE)

#-- Initialise the clock
clock = pygame.time.Clock()

#-- Initialise the physics engine
space = pymunk.Space()
space.gravity = (0.0,  0.0)

#-- Import from the ctf framework
import ai
import boxmodels
import gameobjects
import maps


#-- Constants
framerate = 60
#-- Variables
#   List of all game objects
game_objects_list   = []
game_objects_def_pos_list = []
tanks_list          = []
ais 				= []
box_dict			= {}
exp_list			= []
text_list 			= []
exp_time			= []
tank_exp_list		= []
text_surf_list 		= []
text_rect_list 		= []
player_text_surf_list=[]
player_text_rect_list=[]
art_surf_list 		= []
art_rect_list 		= []
score_surf_list		= []
dead_start_list 	= []
current_map 		= []
portal_list 		= []
text_count_list		= []
powerupish			= []
hoover_list 		= [False, False, False, False]
tanks_color_list	= [(208,137,13,255), (13,91,208,255), (255,255,255,255), \
					(215,227,23,255), (198,41,10,255), (123,123,123,255)]
art_packs_list 		= ["standard", "potato"]
art_pack 			= "standard"
players 			= 0
win_score			= 10
#   Define the current level
pygame.display.set_caption('Capture the Flag')
screen_x = 800
screen_y = 600
#font_x 	= screen_x/2
#font_y  = screen_y/2
font_size = 115
art_font_size = 70
text_font = 'freesansbold.ttf'
text_y = 115
map_nr = 1
screen = pygame.display.set_mode((screen_x,screen_y))
score_font_size = 25
player_score_text = pygame.font.Font(text_font, score_font_size)


def set_art_pack(pack):
	pack_file = open("data/pack_file.txt", "w")
	pack_file.write(str(pack))
	pack_file.close()
	global art_pack
	if art_pack == str(pack):
		pass
	else:
		art_pack = str(pack)


def text_objects(text, font, color = (255,255,255, 1)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


for i in range(3):
	player_largeText = pygame.font.Font(text_font, int(font_size*0.6))
	player_TextSurf, player_TextRect = text_objects("number of players: " + str(players), player_largeText)
	player_TextRect.center = ((screen_x/2), text_y)
	player_text_surf_list.append(player_TextSurf)
	player_text_rect_list.append(player_TextRect)
	text_y += 115
	players += 1
	screen.blit(player_TextSurf, player_TextRect)

players = 1
text_y = 115
choose_players = True


for player_TextRect in player_text_rect_list:
	index = player_text_rect_list.index(player_TextRect)
	mouse = pygame.mouse.get_pos()
	screen.blit(player_text_surf_list[index], player_text_rect_list[index])
	# --- SOUND ---
	pygame.mixer.init()
	pygame.mixer.music.load("data/test2.wav")
	pygame.mixer.music.play()

while choose_players == True:
	

	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			choose_players = False
			pygame.quit()
			quit()
		for player_TextRect in player_text_rect_list:
			index = player_text_rect_list.index(player_TextRect)
			mouse = pygame.mouse.get_pos()
			if player_TextRect.collidepoint(mouse):
				if not hoover_list[index]:
					hoover_list[index] = True
					player_TextSurf = text_objects("number of players: " + str(index), player_largeText, (150,150,150,1))[0]
					screen.blit(player_TextSurf, player_TextRect)
					pygame.display.update()
				if event.type == pygame.MOUSEBUTTONDOWN:
					players = int(index)
					choose_players = False
			elif not player_TextRect.collidepoint(mouse) and hoover_list[index]:
				hoover_list[index] = False
				player_TextSurf = text_objects("number of players: " + str(index), player_largeText)[0]
				screen.blit(player_TextSurf, player_TextRect)
				pygame.display.update()			
			if event.type == KEYDOWN and event.key == (index+48):
				players = int(index)
				choose_players = False
	pygame.display.update()

screen.fill((0,0,0,1))
hoover_list 		= [False, False, False, False]

map_nr = 1
for i in maps.maps_list:
	largeText = pygame.font.Font(text_font, font_size)
	TextSurf, TextRect = text_objects("Play map: " + str(map_nr), largeText)
	TextRect.center = ((screen_x/2), text_y)
	text_surf_list.append(TextSurf)
	text_rect_list.append(TextRect)
	text_y += 115
	map_nr += 1
	screen.blit(TextSurf, TextRect)
map_nr = 1

for TextRect in text_rect_list:
	index = text_rect_list.index(TextRect)
	mouse = pygame.mouse.get_pos()
	screen.blit(text_surf_list[index], text_rect_list[index])
start_menu = True

while start_menu == True:
	

	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			start_menu = False
			pygame.quit()
			quit()
		for TextRect in text_rect_list:
			index = text_rect_list.index(TextRect)
			mouse = pygame.mouse.get_pos()
			if TextRect.collidepoint(mouse):
				if not hoover_list[index]:
					hoover_list[index] = True
					TextSurf = text_objects("Play map: " + str(index+1), largeText, (150,150,150,1))[0]
					screen.blit(TextSurf, TextRect)
					pygame.display.update()


				if event.type == pygame.MOUSEBUTTONDOWN:
					 #screen_x > mouse[0] > 0 and (screen_y + font_size)/2 > mouse[1] > (screen_y - font_size)/2:
					start_menu = False
					current_map = maps.maps_list[index]

			elif not TextRect.collidepoint(mouse) and hoover_list[index]:
				hoover_list[index] = False
				TextSurf = text_objects("Play map: " + str(index+1), largeText)[0]
				screen.blit(TextSurf, TextRect)
				pygame.display.update()


			if event.type == KEYDOWN and event.key == (index+49):
				start_menu = False
				current_map = maps.maps_list[index]

			#make_stuff(screen_x, text_y, map_nr)
		#	else: 
			#	text_surf_list[index].
	pygame.display.update()




screen.fill((0,0,0,1))
hoover_list 		= [False, False, False, False]

text_y = 115

for i in range(len(art_packs_list)):
	largeText = pygame.font.Font(text_font, art_font_size)
	TextSurf, TextRect = text_objects("Art pack: " + str(art_packs_list[i]), largeText)
	TextRect.center = ((screen_x/2), text_y)
	art_surf_list.append(TextSurf)
	art_rect_list.append(TextRect)
	text_y += 115
	screen.blit(TextSurf, TextRect)

for TextRect in art_rect_list:
	index = art_rect_list.index(TextRect)
	mouse = pygame.mouse.get_pos()
	screen.blit(art_surf_list[index], art_rect_list[index])

art_menu = True

while art_menu == True:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			art_menu = False
			pygame.quit()
			quit()
		for TextRect in art_rect_list:
			index = art_rect_list.index(TextRect)
			mouse = pygame.mouse.get_pos()
			if TextRect.collidepoint(mouse):
				if not hoover_list[index]:
					hoover_list[index] = True
					TextSurf = text_objects("Art pack: " + str(art_packs_list[index]), largeText, (150,150,150,1))[0]
					screen.blit(TextSurf, TextRect)
					pygame.display.update()


				if event.type == pygame.MOUSEBUTTONDOWN:
					 #screen_x > mouse[0] > 0 and (screen_y + font_size)/2 > mouse[1] > (screen_y - font_size)/2:
					art_menu = False
					set_art_pack(art_packs_list[index])
					art_pack = art_packs_list[index]
					print(art_pack)

			elif not TextRect.collidepoint(mouse) and hoover_list[index]:
				hoover_list[index] = False
				TextSurf = text_objects("Art pack: " + str(art_packs_list[index]), largeText)[0]
				screen.blit(TextSurf, TextRect)
				pygame.display.update()
	pygame.display.update()

screen.fill((0,0,0,1))

# --- SOUND ---
pygame.mixer.music.stop()
pygame.mixer.music.load("data/glass.wav")
pygame.mixer.music.play()


#-- Resize the screen to the size of the current level
screen = pygame.display.set_mode(current_map.rect().size)
import images

# --- Fence around the map START ---
nw_box = pymunk.Body()
se_box = pymunk.Body()
north_seg = pymunk.Segment(nw_box,  (-0.5, -0.5), (current_map.width + 0.5, -0.5), 0.5)
east_seg = pymunk.Segment(se_box, (current_map.width + 0.5, current_map.height + 0.5),(current_map.width + 0.5, -0.5), 0.5)
south_seg = pymunk.Segment(se_box,  (current_map.width + 0.5, current_map.height + 0.5),(-0.5 , current_map.height + 0.5), 0.5)
west_seg = pymunk.Segment(nw_box,   (-0.5, -0.5), (-0.5, current_map.height + 0.5), 0.5)
north_seg.collision_type = 10
east_seg.collision_type = 10
south_seg.collision_type = 10
west_seg.collision_type = 10
space.add(north_seg, east_seg, south_seg, west_seg)
# --- Fence around the map END ---

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
		grass = pygame.transform.scale(images.grass,(images.TILE_SIZE, images.TILE_SIZE))
		background.blit(grass, (x*images.TILE_SIZE, y*images.TILE_SIZE))


# --- Creation of objects START ---
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
		
		if box_type == 6:
			powerupish.append(gameobjects.Powerup(x+0.5, y+0.5))
			game_objects_list.append(powerupish[-1])

		# If the box model is non nyll, create a box
		elif(box_model != None):
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
				box.hp = 3
			elif box_type == 5:
				box.shape.collision_type = 4
				points  = [[-0, -0], [-0, 0],[0, 0],[0, -0]]
				box.shape = pymunk.Poly(box.body, points)
				portal_list.append(box)

			box_dict[(x+0.5, y+0.5)] = box
			game_objects_list.append(box)

# Create the tanks
# Loop over the starting position

for i in range(0, len(current_map.start_positions)):
	# Get the starting position of the tank "i"
	pos = current_map.start_positions[i]
	# Create the tank, images.tank contains the image
	tank = gameobjects.Tank(pos[0], pos[1], pos[2], images.tanks[i], space)
	

	# Add the tanks base to the map and game_objects_list
	base = gameobjects.GameVisibleObject(pos[0],pos[1], pygame.transform.scale(images.bases[i], \
		(images.bases[i].get_width()*images.IM_SCALE, images.bases[i].get_height()*images.IM_SCALE)))
	# Add the tanks hp bar
	tank.hp_vis += [gameobjects.HP(pos[0]-0.2, pos[1]+0.25)]
	tank.hp_vis += [gameobjects.HP(pos[0]+0.2, pos[1]+0.25)]

	# Add the tank to the list of objects to display
	game_objects_list.append(tank)
	game_objects_list.append(base)
	for hp in tank.hp_vis:
		game_objects_list.append(hp)
	# Add the tank to the list of tanks
	tanks_list.append(tank)
	# Add the tanks overheat image to list
	game_objects_list.append(tanks_list[i].oh)
	# Add the tanks spawn protection image to list
	game_objects_list.append(tanks_list[i].sp)
	# Add score counter:
	TextSurf_counter, TextRect_counter = text_objects(str(tanks_list[i].score), player_score_text)
	counter_text = gameobjects.GameVisibleObject(tank.x_pos, tank.y_pos-0.5, TextSurf_counter)
	text_count_list.append(counter_text)
	game_objects_list.append(counter_text)	

	#Add ai
	if i > (players-1):
		ais.append(ai.SimpleAi(tanks_list[i], game_objects_list, tanks_list, space))

# This function call creates a new flag object at coordinates x, y
flag = gameobjects.Flag(current_map.width/2, current_map.height/2)
game_objects_list.append(flag)
game_objects_def_pos_list = list(game_objects_list)
# --- Creation of objects END ---

def default_pos(tile):
	return tile in game_objects_def_pos_list

# Collision handlers and functions ----START----

def tank_explosion(tank_or_box, image):
	tank_pos = tank_or_box.body.position
	exp = gameobjects.GameVisibleObject(tank_pos[0] , tank_pos[1], pygame.transform.scale(image, (image.get_height()*images.IM_SCALE, image.get_width()*images.IM_SCALE)))
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

def missile_hit(space, arb):
	tank_exp_list.append(tank_explosion(arb.shapes[1].parent, images.small_explosion))
	if arb.shapes[0].parent in game_objects_list:
			space.add_post_step_callback(space.remove, arb.shapes[0], arb.shapes[0].body)
			game_objects_list.remove(arb.shapes[0].parent)
	if arb.shapes[1].parent in game_objects_list:
			space.add_post_step_callback(space.remove, arb.shapes[1], arb.shapes[1].body)
			game_objects_list.remove(arb.shapes[1].parent)
	return 1

def tank_hit(space, arb):
	if not arb.shapes[1].parent == arb.shapes[0].parent.tank and not arb.shapes[1].parent.is_protected:
		arb.shapes[1].parent.hp -= 1
		if arb.shapes[0].parent.tank.powerup and arb.shapes[0].parent.tank.powerup == gameobjects.Powerup.sticky_ammo:
			arb.shapes[1].parent.powerup = gameobjects.Powerup.speed_down
			arb.shapes[1].parent.activate()
		if arb.shapes[0].parent.tank.powerup and arb.shapes[0].parent.tank.powerup == gameobjects.Powerup.damage_up:
			arb.shapes[1].parent.hp -= 1
		if arb.shapes[1].parent.hp == 1:
			tank_exp_list.append(tank_explosion(arb.shapes[1].parent, images.small_explosion))
			game_objects_list.remove(arb.shapes[1].parent.hp_vis[0])
		elif arb.shapes[1].parent.hp <= 0:
			arb.shapes[0].parent.tank.kills_increment(arb.shapes[1].parent)
			if arb.shapes[1].parent.powerup:
				arb.shapes[1].parent.deactivate()
			#arb.shapes[1].parent.score_red()
			global current_map
			for index in range(len(tanks_list)):
				if 	tanks_list[index].hp == 0:
					player_dead = gameobjects.GameVisibleObject(current_map.width/2,current_map.height/2 , images.was_killed[index])
					dead_start_list.append(time.time())
					game_objects_list.append(player_dead)
					text_list.append(player_dead)
			if arb.shapes[1].parent.flag != None:
				flag_x = arb.shapes[1].parent.x_pos
				flag_y = arb.shapes[1].parent.y_pos
				arb.shapes[1].parent.flag = None
				flag = gameobjects.Flag(flag_x, flag_y)	
			tank_exp_list.append(tank_explosion(arb.shapes[1].parent, images.explosion))
			arb.shapes[1].parent.body.position = arb.shapes[1].parent.start_position
			arb.shapes[1].parent.body.angle = arb.shapes[1].parent.start_orientation
			arb.shapes[1].parent.hp = 2
			arb.shapes[1].parent.maximum_speed = arb.shapes[1].parent.default_max_speed
	if not arb.shapes[1].parent == arb.shapes[0].parent.tank and arb.shapes[0].parent in game_objects_list:
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

def tank_portal(space, arb):
	if not arb.shapes[0].parent.is_portal_cd:
		pos = random.choice(portal_list)
		arb.shapes[0].parent.body.position = pymunk.Vec2d(pos.x_pos, pos.y_pos)
		arb.shapes[0].parent.is_portal_cd = True

		#tank.portal_time = 0
	return 1

def other_hit(space, arb):
	if arb.shapes[0].parent in game_objects_list:
		tank_exp_list.append(tank_explosion(arb.shapes[0].parent, images.small_explosion))
		space.add_post_step_callback(space.remove, arb.shapes[0], arb.shapes[0].body)
		game_objects_list.remove(arb.shapes[0].parent)
	return 1

space.add_collision_handler(0, 0, None, missile_hit)
space.add_collision_handler(0, 1, None, tank_hit)
space.add_collision_handler(0, 2, None, box_hit)
space.add_collision_handler(1, 4, None, tank_portal)
space.add_collision_handler(0, 10, None, other_hit)
space.add_collision_handler(0, 4, None, other_hit)

# Collision handlers and functions ----END----



#----- Main Loop -----#

#-- Control whether the game should run
running = True
exp_start = 0
start = 0
skip_update = 0
score_text = pygame.font.SysFont(text_font, 30)
#tab_text = pygame.font.SysFont("Arial", 40)
paused = False
counter_index = 0
screen_x = current_map.width*images.TILE_SIZE
#tab_overlay = pygame.draw.rect(screen, (0,0,0), ((0,0), (screen_x,screen_y)), 1)
#tab_x = 100*images.IM_SCALE
#tab_y  = 100 * images.IM_SCALE
while running:
	# --- SOUND ---
	if not pygame.mixer.music.get_busy():
		pygame.mixer.music.load("data/gun.wav")
		pygame.mixer.music.play()
		pygame.mixer.music.set_volume(0.3)

	#-- Handle the events
	for event in pygame.event.get():
		# Check if we receive a QUIT event (for instance, if the user press the
		# close button of the window) or if the user press the escape key.
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			running = False
		if players > 0:	
			if event.type == KEYDOWN and event.key == K_p:
				paused = True
				game_paused = gameobjects.GameVisibleObject(current_map.width/2,current_map.height/2 , images.pause)
				game_objects_list.append(game_paused)
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
				#if not tanks_list[0].start or time.time() > tanks_list[0].start + 2:
				if tanks_list[0].is_overheated:
					player_dead = gameobjects.GameVisibleObject(current_map.width/2,current_map.height/2 , images.died_to_oh[0])
					dead_start_list.append(time.time())
					game_objects_list.append(player_dead)
					text_list.append(player_dead)
					if tanks_list[0].powerup:
						tanks_list[0].deactivate()
				game_objects_list.append(gameobjects.Tank.shoot(tanks_list[0], space)[0])
		if players > 1:
			if event.type == KEYDOWN and event.key == K_w:
				gameobjects.Tank.accelerate(tanks_list[1])
			elif event.type == KEYUP and event.key == K_w:
				gameobjects.Tank.stop_moving(tanks_list[1])
			if event.type == KEYDOWN and event.key == K_s:
				gameobjects.Tank.decelerate(tanks_list[1])
			elif event.type == KEYUP and event.key == K_s:
				gameobjects.Tank.stop_moving(tanks_list[1])
			if event.type == KEYDOWN and event.key == K_a:
				gameobjects.Tank.turn_left(tanks_list[1])
			elif event.type == KEYUP and event.key == K_a:
				gameobjects.Tank.stop_turning(tanks_list[1])
			if event.type == KEYDOWN and event.key == K_d:
				gameobjects.Tank.turn_right(tanks_list[1])
			elif event.type == KEYUP and event.key == K_d:
				gameobjects.Tank.stop_turning(tanks_list[1])
			if event.type == KEYDOWN and event.key == K_SPACE:
				if tanks_list[1].is_overheated:
					player_dead = gameobjects.GameVisibleObject(current_map.width/2,current_map.height/2 , images.died_to_oh[1])
					dead_start_list.append(time.time())
					game_objects_list.append(player_dead)
					text_list.append(player_dead)
					if tanks_list[1].powerup:
						tanks_list[1].deactivate()
				game_objects_list.append(gameobjects.Tank.shoot(tanks_list[1], space)[0])

	#		if event.type == KEYDOWN and event.key == K_SPACE:
	#			screen2 = screen
	#			screen = pygame.display.set_mode((1000, 1000),RESIZABLE)
	#			pygame.transform.scale(screen2, (1000, 1000), screen)
	#			pygame.display.flip()


	for tank in tanks_list:
		if tank.hp == 2 and not tank.hp_vis[0] in game_objects_list:
			game_objects_list.append(tank.hp_vis[0])
		if tank.hp == 1 and tank.hp_vis[0] in game_objects_list:
			game_objects_list.remove(tank.hp_vis[0])
		game_objects_list.remove(text_count_list[counter_index])
		counter_x = tank.body.position[0] - 0.4
		counter_y = tank.body.position[1] - 0.4
		TextSurf_counter, TextRect_counter = text_objects(str(tank.score), player_score_text)
		counter = gameobjects.GameVisibleObject(counter_x, counter_y, TextSurf_counter)
		text_count_list[counter_index] = counter
		game_objects_list.append(text_count_list[counter_index])
		counter_index += 1
	counter_index = 0


			

	if tank_exp_list and tank_exp_list[0]():
		tank_exp_list.pop(0)

	for tank in tanks_list:
		if tank.is_overheated and time.time() > tank.start + 2:
			tank.is_overheated = False
		if tank.is_portal_cd and time.time() > tank.portal_time + 3:
			tank.is_portal_cd = False
			tank.portal_time = time.time()
		if tank.death_timer+4 < time.time():
			tank.is_protected = False
		if tank.powerup and tank.powerup_timer + 10 < time.time():
			tank.deactivate()

		#player_largeText = pygame.font.Font(text_font, int(font_size*0.6))
		#player_TextSurf, player_TextRect = text_objects("number of players: " + str(players), player_largeText)
		#player_TextRect.center = ((screen_x/2), text_y)

				
		#score_rect = text_objects(str(tank.score), score_text)[1]
		#score_surf_list.append(score_surf)
		#screen.blit(score_surf, score_rect)  #, (tank.x_pos - 0.2*images.IM_SCALE, tank.y_pos - 0.2*images.IM_SCALE))
		#score_surf = score_text.render(str(tank.score), True, (255,255,255,1))
		#screen.blit(score_surf, (1,2))

	if dead_start_list and time.time() > dead_start_list[0] + 1:
		game_objects_list.remove(text_list.pop(0))
		dead_start_list.pop(0)

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
		for power in powerupish:
			if not tanks_list[i].powerup:
				tanks_list[i].try_grab_powerup(power)
		if tanks_list[i].score >= win_score:
			running = False
		elif gameobjects.Tank.has_won(tanks_list[i]):
			tanks_list[i].score_increment(3)
			tanks_list[i].flag = None
			flag.is_on_tank = False
			flag.reset_flag()
			tanks_list[i].maximum_speed = tanks_list[i].default_max_speed
		if i < len(tanks_list)-players:
			ai.SimpleAi.decide(ais[i])
		if tanks_list[i].is_powered_up and tanks_list[i].powerup and tanks_list[i].powerup_timer and tanks_list[i].powerup_timer+10 < time.time():
			tanks_list[i].deactivate()
			#tanks_list[i].is_powered_up = False
			#tanks_list[i].powerup = None
			#powerupish = gameobjects.Powerup(0.5, 1.5)
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

	while paused:
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_u:
				paused = False
				game_objects_list.remove(game_paused)


Win_Screen = True
text_y = 100
font_size = 50

rectangle = pygame.draw.rect(screen, (0,0,0), ((0,0), (2000,2000)), 1)
screen.blit(images.overlay, rectangle)
player_largeText = pygame.font.Font(text_font, font_size)

for tank in tanks_list:
	
	player_TextSurf, player_TextRect = text_objects("Player " + str(tanks_list.index(tank)+1) + " score: " + \
		str(tank.score), player_largeText, tanks_color_list[tanks_list.index(tank)])
	player_TextRect.center = ((screen_x/2), text_y)
	player_text_surf_list.append(player_TextSurf)
	player_text_rect_list.append(player_TextRect)
	text_y += 60
	screen.blit(player_TextSurf, player_TextRect)

text_y += 100
player_TextSurf, player_TextRect = text_objects("Press ESC to quit", player_largeText)
player_TextRect.center = ((screen_x/2), text_y)
screen.blit(player_TextSurf, player_TextRect)

while Win_Screen:
	for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				Win_Screen = False
	pygame.display.update()
