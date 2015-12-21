import images
import pygame
import pymunk
import math
import boxmodels
import time
import random


# This function is used to convert coordinates in the physic engine into the display coordinates
def physics_to_display(x):
  return x * images.TILE_SIZE

# Define an object (tank, flags, box...) in the game. This class mostly handle visual aspects of
# objects.
#
# Subclass need to implement two functions:
# * screen_position    that will return the position of the object on the screen
# * screen_orientation that will return how much the object is rotated on the screen (in degrees)
class GameObject:
  #
  # Object are 
  #
  def __init__(self, sprite):
    self.sprite         = sprite
  #
  # This function is called for objects to update their state.
  #
  # Can be reimplemented in a subclass.
  #
  def update(self):
    return
  #
  # This function is called after all objects have updated their state,
  # and it can be used by objects whose state depends on the state of
  # a different object.
  #
  # Can be reimplemented in a subclass.
  #
  def post_update(self):
    return
  #
  # This function is called to draw the object on the screen.
  #
  # You should not need to reimplement this function in a subclass.
  #
  def update_screen(self, screen):
    sprite = self.sprite
    # Get the position of the object
    p      = self.screen_position()
    # Rotate the sprite using the rotation of the object
    sprite = pygame.transform.rotate(sprite, self.screen_orientation())
    # The position of the screen correspond to the center of the object,
    # but the function screen.blit expect to receive the top left corner
    # as argument, so we need to adjust the position p with an offset
    # which is the vector between the center of the sprite and the top left
    # corner of the sprite.
    offset = pymunk.Vec2d(sprite.get_size()) / 2.
    p = p - offset
    # Copy the sprite on the screen
    screen.blit(sprite, p)
    # debug draw
    #ps = self.shape.get_points()
    #ps = [physics_to_display(p) for p in ps]
    #ps += [ps[0]]
    #pygame.draw.lines(screen, pygame.color.THECOLORS["red"], False, ps, 1)

#
# This class extends GameObject and it is used for objects which have a
# physical shape (such as tanks and boxes). This class handle the physical
# interaction of the objects.
#
class GamePhysicsObject(GameObject):
  #
  # Taks as parameters the starting coordinate (x,y), the orientation, the sprite (aka the image
  # representing the object), the physic engine object (space) and whether the object can be
  # moved (movable).
  #
  def __init__(self, x, y, orientation, sprite, space, movable):
    GameObject.__init__(self, sprite)
    # Initialise the physics body
    # Half dimensions of the object converted from screen coordinates to physic coordinates
    half_width          = 0.5 * self.sprite.get_width() / images.TILE_SIZE
    half_height         = 0.5 * self.sprite.get_height() / images.TILE_SIZE
    # In this game, physical objects have a rectangular shape, the variable points contains the points
    # corresponding to the corner of that shap.
    points              = [[-half_width, -half_height],
                           [-half_width, half_height],
                           [half_width, half_height],
                           [half_width, -half_height]]
    # Create a body (which is the physical representation of this game object in the physic engine)

    if(movable):
      # Create a movable object with some mass and moments
      # (considering the game is a top view game, with no gravity,
      # the mass is set to the same value for all objects)
      mass = 50
      moment = pymunk.moment_for_poly(mass, points)
      self.body         = pymunk.Body(mass, moment)
    else:
      # Create a non movable object
      self.body         = pymunk.Body()
    
    # Initialize the body position and angle
    self.body.position  = x, y
    self.body.angle     = math.radians(orientation)
    # Create a polygon shape using the corner of the rectangle
    self.shape          = pymunk.Poly(self.body, points)
    self.shape.parent   = self
    # Set some value for friction and elasticity, which defines interraction in case of a colision
    self.shape.friction = 1
    self.shape.elasticity = 0.1

    # Add the object to the physic engine
    if(movable):
      space.add(self.body, self.shape)
    else:
      space.add(self.shape)


  def screen_position(self):
    # screen_position is defined by the body position in the physic engine
    return physics_to_display(self.body.position)
  
  def screen_orientation(self):
    # Angle are reversed in the engine and in display
    return -math.degrees(self.body.angle)

  # Convenient function to bound a value to a specific interval
def clamp (minval, val, maxval):
  if val < minval: return minval
  if val > maxval: return maxval
  return val

#
# This class extends GamePhysicsObject to handle aspects which are specific to tanks.
#
class Tank(GamePhysicsObject):
  def __init__(self, x, y, orientation, sprite, space):
    sprite = pygame.transform.scale(sprite, (int(images.TILE_SIZE//1.7), \
    int(images.TILE_SIZE//1.7)))
    GamePhysicsObject.__init__(self, x, y, orientation, sprite, space, True)
    # Define all properties related to a Tank object.
    self.acceleration         = 0.0
    self.velocity             = 0.0
    self.angular_acceleration = 0.0
    self.angular_velocity     = 0.0
    self.orientation          = orientation
    self.flag                 = None
    self.default_max_speed    = 2
    self.maximum_speed        = 2
    self.x_pos                = x
    self.y_pos                = y
    self.sprite               = sprite 
    self.shape.collision_type = 1 
    self.hp                   = 2
    self.hp_vis               = []
    self.start                = 0
    self.is_overheated        = False
    self.is_portal_cd         = False
    self.portal_time          = 0
    self.score                = 0
    self.oh                   = GameVisibleObject(self.x_pos, self.y_pos, \
    pygame.transform.scale(images.overheat,(images.TILE_SIZE, images.TILE_SIZE)))
    self.death_timer          = 0
    self.is_protected         = False
    self.sp                   = GameVisibleObject(self.x_pos, self.y_pos, \
    pygame.transform.scale(images.spawn_protect,(images.TILE_SIZE, images.TILE_SIZE)))
    self.kills                = 0
    self.deaths               = 0
    self.powerup              = None
    self.is_powered_up        = False
    self.powerup_timer        = 0
    self.damage               = 1
    self.start_position       = pymunk.Vec2d(self.x_pos, self.y_pos)
    self.start_orientation    = orientation

  def score_increment(self, score_inc=1):
    self.score += score_inc


  def score_red(self):
    self.score -= 2
    if self.score < 0:
      self.score = 0
    self.is_protected = True
    self.death_timer = time.time()


  def kills_increment(self, tank):
    self.kills += 1
    self.score_increment()
    tank.deaths_increment()


  def deaths_increment(self):
    self.deaths += 1
    self.score_red()


  # Call this function to accelerate forward the tank
  def accelerate(self):
    self.acceleration = 0.2
  

  # Call this function to accelerate backward the tank
  def decelerate(self):
    self.acceleration = -0.2
  

  # Call this function to start turning in the left direction
  def turn_left(self):
    self.angular_acceleration = -1
  

  # Call this function to start turning in the right direction
  def turn_right(self):
    self.angular_acceleration = 1
  

  def update(self):
    # Update the velocity of the tank in function of the physic simulation (in case of colision, the physic simulation will change the speed of the tank)
    if(math.fabs(self.velocity) > 0 ):
      self.velocity         *= self.body.velocity.length  / math.fabs(self.velocity)
    if(math.fabs(self.angular_velocity) > 0 ):
      self.angular_velocity *= math.fabs(self.body.angular_velocity / self.angular_velocity)
    
    # Update the velocity in function of the acceleration
    self.velocity         += self.acceleration
    self.angular_velocity += self.angular_acceleration
    
    # Make sure the velocity is not larger than a maximum speed
    self.velocity         = clamp(-self.maximum_speed, self.velocity,         self.maximum_speed)
    self.angular_velocity = clamp(-self.maximum_speed, self.angular_velocity, self.maximum_speed)
    
    # Update the physic velocity
    self.body.velocity = pymunk.Vec2d((0, self.velocity)).rotated(self.body.angle)
    self.body.angular_velocity = self.angular_velocity
  

  # Call this function to make the tank stop moving
  def stop_moving(self):
    self.velocity     = 0
    self.acceleration = 0
  

  # Call this function to make the tank stop turning
  def stop_turning(self):
    self.angular_velocity     = 0
    self.angular_acceleration = 0
  

  def post_update(self):
    # If the tank carries the flag, then update the positon of the flag.
    if(self.flag != None):
      self.flag.x           = self.body.position[0]
      self.flag.y           = self.body.position[1]
      self.flag.orientation = -math.degrees(self.body.angle)

    # Handles the displaying of the overheat overlay for a tank.
    if self.is_overheated:
      self.oh.x           = self.body.position[0]
      self.oh.y           = self.body.position[1]
    else:
      self.oh.x           = 1337
      self.oh.y           = 1337 

    # Handles the displaying of the shield overlay for a tank.
    if self.is_protected:
      self.sp.x           = self.body.position[0]
      self.sp.y           = self.body.position[1]
    elif not self.is_protected:
      self.sp.x           = 1337
      self.sp.y           = 1337 
   

  # Call this function to try to grab the flag, if the flag is not on other tank
  # and it is close to the current tank, then the current tank will grab the flag
  def try_grab_flag(self, flag):
    # Check that the flag is not on other tank
    if(not flag.is_on_tank):
      #  Check if the tank is close to the flag
      flag_pos = pymunk.Vec2d(flag.x, flag.y)
      if((flag_pos - self.body.position).length < 0.5):
        # Grab the flag !
        self.flag           = flag
        self.is_on_tank     = True
        self.maximum_speed  = 3

  # Call this function to try to grab a powerup.
  # If it is close to the current tank, then the current tank will get said powerup.
  def try_grab_powerup(self, powerup):
    powerup_pos = pymunk.Vec2d(powerup.x_pos, powerup.y_pos)
    if not self.is_powered_up:
      if((powerup_pos - self.body.position).length < 0.5):
        self.powerup = Powerup.random_powerup()
        print(self.powerup)
        self.activate()
    else: 
      if((powerup_pos - self.body.position).length < 0.5):
        self.deactivate()
        self.powerup = Powerup.random_powerup()
        self.activate()


  def activate(self):
    self.powerup(self, True)
    self.powerup_timer = time.time()
    

  def deactivate(self):
    self.powerup(self, False)
    self.is_powered_up = False


  # Check if the current tank has captured the flag (if it has the flag and it is close to its start position)
  def has_won(self):
    return self.flag != None and (self.start_position - self.body.position).length < 0.2


  # Call this function to shoot.
  def shoot(self, space):
    if self.powerup and self.powerup == Powerup.sticky_ammo: 
      missile = Missile(self.body.position[0], self.body.position[1], \
      math.degrees(self.body.angle), images.sticky_missile, space, self)
    else:
      missile = Missile(self.body.position[0], self.body.position[1], \
      math.degrees(self.body.angle), images.missile, space, self)
    self.velocity = -1
    Tank.update(missile)
    if self.is_overheated: 
      self.flag = None
      self.body.position[0] = self.start_position[0]
      self.body.position[1] = self.start_position[1]
      self.body.angle = self.start_orientation
      self.is_overheated = False
      self.maximum_speed = self.default_max_speed
      self.hp = 2
      self.deaths_increment()
      return (missile, self.start, self)
    if not self.powerup or self.powerup != Powerup.automatic_fire:
      self.is_overheated = True
      self.start = time.time()
    return (missile, self.start, self)


# This class extends the GamePhysicsObject to handle box objects.
#
class Box(GamePhysicsObject):
  #
  # It takes as arguments the coordinate of the starting position of the box (x,y) and the box model (boxmodel).
  #
  def __init__(self, x, y, boxmodel, space):
    self.boxmodel = boxmodel
    GamePhysicsObject.__init__(self, x, y, 0, pygame.transform.scale(self.boxmodel.sprite, \
    (images.TILE_SIZE, images.TILE_SIZE)), space, self.boxmodel.movable)
    self.shape.collision_type = 10
    self.hp                   = -1
    self.x_pos                = x
    self.y_pos                = y
    self.dead                 = False
#
# This class extends GameObject for object that are visible on screen but have no physical representation (bases and flag)
#

class GameVisibleObject(GameObject):
  #
  # It takes argument the coordinates (x,y) and the sprite.
  #
  def __init__(self, x, y, sprite):
    self.x            = x
    self.y            = y
    self.orientation  = 0
    GameObject.__init__(self, sprite)


  def screen_position(self):
    return physics_to_display(pymunk.Vec2d(self.x, self.y))


  def screen_orientation(self):
    return self.orientation


#
# This class extends GameVisibleObject for representing flags.
#
class Flag(GameVisibleObject):
  def __init__(self, x, y):
    self.is_on_tank   = False
    GameVisibleObject.__init__(self, x, y,  pygame.transform.scale(images.flag, \
    (images.TILE_SIZE, images.TILE_SIZE)))
    self.start_pos = (x,y)


  def reset_flag(self):
    self.x, self.y = self.start_pos
    self.orientation = 0


class Powerup(GameVisibleObject):
  def __init__(self, x, y, powerup_kind= None):
  	# Define the properties of a pwerup object
    self.type_img = images.load_image('powerup.png')
    self.sprite = pygame.transform.scale(self.type_img, (images.TILE_SIZE, images.TILE_SIZE))
    self.x_pos = x
    self.y_pos = y
    self.timer = 0
    self.powerup_timer = 20
    GameVisibleObject.__init__(self, x, y, self.sprite)


  def random_powerup():
    return random.choice([Powerup.speed_up, Powerup.damage_up, Powerup.shield, Powerup.speed_down, \
    Powerup.extreme_overheat, Powerup.sticky_ammo, Powerup.automatic_fire])


  def speed_up(tank, value):
    # Activate
    if value:
      tank.maximum_speed = 3
    # Deactivate
    else:
      tank.maximum_speed = tank.default_max_speed
      tank.powerup = None
    tank.is_powered_up = value


  def damage_up(tank, value):
    if value:
      tank.damage = 2
    else:
      tank.damage = 2
      tank.powerup = None
    tank.is_powered_up = value


  def shield(tank, value):
    if value:
      tank.death_timer = time.time() + 5
      tank.is_protected = True
    else:
      tank.powerup = None
    tank.is_powered_up = value


  def speed_down(tank, value):
    if value:
      tank.maximum_speed = 1
    else:
      tank.maximum_speed = tank.default_max_speed
      tank.powerup = None
    tank.is_powered_up = value


  def extreme_overheat(tank, value):
    if value:
      tank.start = time.time() + 8
      tank.is_overheated = True
    else:
      tank.powerup = None
    tank.is_powered_up = value


  def sticky_ammo(tank, value):
    if not value:
      tank.powerup = None
    tank.is_powered_up = value


  def automatic_fire(tank, value):
    if not value:
      tank.powerup = None
    tank.is_powered_up = value


class HP(GameVisibleObject):
  def __init__(self, x, y):
  	# Displays the HP of a tank visually.
    GameVisibleObject.__init__(self, x, y,  pygame.transform.scale(images.hp, \
    (10*images.IM_SCALE,10*images.IM_SCALE)))



class Missile(GamePhysicsObject):
  def __init__(self, x, y, orientation, sprite, space, tank):
    GamePhysicsObject.__init__(self, x, y, orientation, sprite, space, True)
    # Define the properties of a missile object
    self.tank                 = tank
    self.orientation          = orientation
    self.acceleration         = 20.0
    self.velocity             = 10.0
    self.angular_acceleration = 0.0
    self.angular_velocity     = 0.0
    self.maximum_speed        = 30.0
    self.shape.collision_type = 0
    self.sprite             = pygame.transform.scale(sprite, (images.TILE_SIZE//2, images.TILE_SIZE//2))
    # Define the start position, which is the position of the shooting tank
    self.start_position       = pymunk.Vec2d(x, y)
