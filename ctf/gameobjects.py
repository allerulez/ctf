import images
import pygame
import pymunk
import math

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
      mass = 10
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
    # Set some value for friction and elasticity, which defines interraction in case of a colision
    self.shape.friction = 0.5
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
    GamePhysicsObject.__init__(self, x, y, orientation, sprite, space, True)
    # Define variable used to apply motion to the tanks
    self.acceleration         = 0.0
    self.velocity             = 0.0
    self.angular_acceleration = 0.0
    self.angular_velocity     = 0.0
    # This variable is used to access the flag object, if the current tank is carrying the flag
    self.flag                 = None
    # Impose a maximum speed to the tank
    self.maximum_speed        = 1.0
    # Define the start position, which is also the position where the tank has to return with the flag
    self.start_position       = pymunk.Vec2d(x, y)
  
  # Call this function to accelerate forward the tank
  def accelerate(self):
    self.acceleration = 0.1
  
  # Call this function to accelerate backward the tank
  def decelerate(self):
    self.acceleration = -0.1
  
  # Call this function to start turning in the left direction
  def turn_left(self):
    self.angular_acceleration = -0.1
  
  # Call this function to start turning in the right direction
  def turn_right(self):
    self.angular_acceleration = 0.1
  
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
    # If the tank carries the flag, then update the positon of the flag
    if(self.flag != None):
      self.flag.x           = self.body.position[0]
      self.flag.y           = self.body.position[1]
      self.flag.orientation = -math.degrees(self.body.angle)
  
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
        self.maximum_speed  = 0.5
  # Check if the current tank has won (if it is has the flag and it is close to its start position)
  def has_won(self):
    return self.flag != None and (self.start_position - self.body.position).length < 0.2
  # Call this function to shoot forward (current implementation does nothing ! you need to implement it yourself)
  def shoot(self, space):
    self.stop_moving()
    self.stop_turning()
    self.velocity = -1
    missile = Missile(self, images.missile, space)


    return

#
# This class extends the GamePhysicsObject to handle box objects.
#
class Box(GamePhysicsObject):
  #
  # It takes as arguments the coordinate of the starting position of the box (x,y) and the box model (boxmodel).
  #
  def __init__(self, x, y, boxmodel, space):
    self.boxmodel = boxmodel
    GamePhysicsObject.__init__(self, x, y, 0, self.boxmodel.sprite, space, self.boxmodel.movable)

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
    GameVisibleObject.__init__(self, x, y,  images.flag)

class Missile(GamePhysicsObject):
  def __init__(self, tank, sprite, space):
    GamePhysicsObject.__init__(self, tank.x, tank.y, tank.orientation, sprite, space, True)
    # Define variable used to apply motion to the tanks
    self.orientation          = tank.orientation
    self.acceleration         = 0.0
    self.velocity             = 2.0
    self.angular_acceleration = 0.0
    self.angular_velocity     = 0.0
    # Define the start position, which is also the position where the tank has to return with the flag
    self.start_position       = pymunk.Vec2d(tank.start_position[0], tank.start_position[1])
 """ This is a nearly functional class, fix it next time """