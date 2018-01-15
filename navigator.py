# Navigator

import math
from utils import *


class Navigator():
    
    ### Path: the planned path of nodes
    ### World: a pointer to the world object
    ### Agent: the agent doing the navigation
    ### source: where starting from
    ### destination: where trying to go
    
    
    def __init__(self):
        self.path = None
        self.agent = None
        self.source = None
        self.destination = None

    
    def setAgent(self, agent):
        self.agent = agent
    
    def setPath(self, path):
        self.path = path

    def getSource(self):
        return self.source
    
    def getDestination(self):
        return self.destination
    
    def getPath(self):
        return self.path

    
    
    ### Callback from Agent. Agent has reached its move target and must determine what to do next.
    ### If the path has been exhausted, the agent moves to the destination. Otherwise, it gets the next waypoint from the path.
    def doneMoving(self):
        # Check that the agent is valid
        if self.agent != None:
            # Check that the path is set
            if self.path != None:
                # If the path length is 0, then the path has been exhausted and it should be safe to move directly to the destination.
                if len(self.path) == 0:
                    # Tell the agent to go to the destination
                    #self.agent.moveToTarget(self.destination)
                    self.path = None
                    self.source = None
                    self.destination = None
                else:
                    # Get the next waypoint and go there instead
                    direction = self.path.pop(0)
                    self.agent.moveOneStep(direction)
                    self.checkpoint()

    ### Called when the agent gets to a node in the path
    ### self: the navigator object
    def checkpoint(self):
        return None
    
    ### Callback from Agent. Agent has collided with something.
    def collision(self, thing):
        print "Collision"
    
    ### This function gets called by the agent to figure out if some shortcutes can be taken when traversing the path.
    ### This function should update the path and return True if the path was updated
    def smooth(self):
        return False
    
    ### Finds the shortest path from the source to the destination. It should minimally set the path.
    ### self: the navigator object
    ### source: the place the agent is starting from (i.e., it's current location)
    ### dest: the place the agent is told to go to
    def computePath(self, source, dest):
        return None

    ### Gets called after every agent.update()
    ### self: the navigator object
    ### delta: time passed since last update
    def update(self, delta):
        return None


###################
### GridNavigator
###
### Abstract base class for navigating the world on a grid.

class GridNavigator(Navigator):


    ### grid: the grid, a 2D array where each element is True or False indicating navigability of that region of the corresponding region of space.
    ### dimensions: the number of columns and rows in the grid: (columns, rows)
    ### cellSize: the physical size of each corresponding cell in the map. Automatically set to the agent's radius x 2.

    def __init__(self):
        Navigator.__init__(self)
        self.grid = None
        self.dimension = None

    def setAgent(self, agent):
        Navigator.setAgent(self, agent)
        self.dimension = agent.world.dimension
        self.grid = agent.world.level

    def estimatedCost(self, current, destination):
        if self.grid == None:
            return None

        return math.fabs(current[0] - destination[0]) + math.fabs(current[1] - destination[1])

    def walkableDirections(self, current):
        if self.grid == None:
            return None
        directions = []
        for d in ['up', 'right', 'down', 'left']:
            loc = getLocation(current, d, 1)
            locValid = locationValid(loc, self.dimension)
            if locValid is False:
                continue
            
            thing = self.grid[loc[1]][loc[0]]
            if thing is not None:
                if thing.health > 100:
                    #print thing.health
                    continue
            directions.append(d)

        return directions


            





################
### GreedyGridNavigator
###
### The GreedyGridNavigator dynamically creates a grid with 4-connectivity
### But when asked to move the agent, it computes a path through the network always moving closer to the destination and probably fails to reach its destination.

class GreedyGridNavigator(GridNavigator):
    
    def __init__(self):
        GridNavigator.__init__(self)
    


    ### Finds the shortest path from the source to the destination. It should minimally set the path.
    ### self: the navigator object
    ### source: the place the agent is starting from (i.e., it's current location)
    ### dest: the place the agent is told to go to
    def computePath(self, source, dest):
        if self.agent != None and source != dest:
            self.source = source
            self.destination = dest
            start = source
            end = dest
            current = start
            self.path = [] # Path holds the grid cells, needs to be translated back to real world coordinates
            count = 0
            last = current
            while current != end and count < 100:
                count = count + 1
                directions = self.walkableDirections(current)
#                last = current
                best = None
                dist = 0
                for direct in directions:
                    d = self.estimatedCost(getLocation(current, direct, 1), end)
                    if best == None or d < dist:
                        best = direct
                        dist = d
                        #print "move ", direct, "dist ", d
                current = getLocation(current, best, 1)
                #print "best = ", best, " loc = ", current
                self.path.append(best)
            #print self.path
