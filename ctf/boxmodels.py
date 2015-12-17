import images

#
# This class defines a model of the box, it contains information on the type of box,
# whether it can be moved, destroyed and the sprite.
#
class BoxModel:
  def __init__(self, sprite, movable, destructable, orientation = None):
    self.sprite         = sprite
    self.movable        = movable
    self.destructable   = destructable
    self.orientation    = orientation

# Define the wood box as movable and destructable
woodbox  = BoxModel(images.woodbox,  True, True)

# Define the metal box as movable and indestructable
metalbox = BoxModel(images.metalbox, True, False)

# Define the rock box (ie wall) as non movable and indestructable
rockbox  = BoxModel(images.rockbox,  False, False)

rockbox_mov = BoxModel(images.rockbox, True, True)

portal_n = BoxModel(images.portal, False, False, 180)
portal_s = BoxModel(images.portal, False, False, 0)
portal_e = BoxModel(images.portal, False, False, 90)
portal_w = BoxModel(images.portal, False, False, 270)


# This function is used to select the model of a box in function of a number.
# It is mostly used when initializing the boxes from the information contained
# in the map.
#   1 is a rockbox
#   2 is a woodbox
#   3 is a metalbox
def get_model(type):
  if(type == 1):
    return rockbox
  elif(type == 2):
    return woodbox
  elif(type == 3):
    return metalbox
  elif(type == 4):
    return rockbox_mov
  elif(type == 5):
    return portal_n
  elif(type == 7):
    return portal_s
  elif(type == 8):
    return portal_e
  elif(type == 9):
    return portal_w
  else:
    return None
