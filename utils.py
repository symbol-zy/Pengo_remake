# Some useful functions


import  pygame, random, time
from constants import *

# load an array of images into a 2-d list
def load_tile_table(filename, width = 32, height = 32, colorkey = BLACK):
    """Load an image and split it into tiles."""
    image = pygame.image.load(filename)
#    image.convert()
    image.set_colorkey(colorkey)
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_x in range(0, image_width/width):
        line = []
        tile_table.append(line)
        for tile_y in range(0, image_height/height):
            rect = (tile_x*width, tile_y*height, width, height)
            line.append(image.subsurface(rect))
    return tile_table



# Element-wise addition on iterable things such as list, tuple etc.,
# and return a tuple.( Vector addition)
def add(s1, s2):
    return tuple(map(lambda x, y: x + y, s1, s2))

def dotProduct(s1, s2):
    return tuple(map(lambda x, y: x * y, s1, s2))


### Distance between two points
def distance(p1, p2):
    return (((p2[0]-p1[0])**2) + ((p2[1]-p1[1])**2))**0.5


# currentLoc and location are world locations (or coordinates)
def getLocation(currentLoc, direction, distance):
    if direction  == 'up':
        location = add(currentLoc, [0, -1 * distance])            
    elif direction  == 'down':
        location = add(currentLoc, [0, distance])  
    elif direction  == 'left':
        location = add(currentLoc, [-1 * distance, 0])  
    elif direction  == 'right':
        location = add(currentLoc,  [distance, 0])  

    return location
    

# Convert world coordinates to screen coordinates 
def worldToScreen(location):
    return dotProduct(location, [GRIDWIDTH, GRIDHEIGHT])

# Convert screen coordinates to world coordinates
def screenToWorld(screenLoc):
    return  (screenLoc[0]/GRIDWIDTH, screenLoc[1]/GRIDHEIGHT)

    


# Return True if the world location is valid, otherwise return False    
def locationValid(location, dimension):
    if location[0] < 0 or location[0] > dimension[0] -1  or location[1] < 0 or location[1] > dimension[0] -1:
        return False
    else:
        return True
    
