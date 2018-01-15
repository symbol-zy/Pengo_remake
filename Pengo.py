# Pengo Remake




###########################

import  pygame, random, time
#from pygame.locals import *
from constants import *
from utils import *
from navigator import *



corerandom = random.Random()

###########################
###########################
### Thing

class Thing(object):

    def update(self, delta):
        return None
        
    def collision(self, thing):
        return None
            
#   def notify(self):
#       return None
  

class Tile(pygame.sprite.Sprite):
    """ The class is the player-controlled sprite. """

    # -- Methods
    def __init__(self, location, image):
        """Constructor function"""
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Set height, width
        self.image = image

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = worldToScreen(self.location)


        

###########################
### Mover

class Mover(pygame.sprite.Sprite, Thing):

        
    ### rect: the rectangle for screen pixel location
    ### location: grid location
    ### image: the current image displaying
    ### frames: image table
    ### direction: direction agent is facing
    ### speed: how fast the agent moves (horizontal, vertical)
    ### world: the world
    ### alive: the agent is alive (boolean)

    def __init__(self, location, direction, speed, frames, world):
        pygame.sprite.Sprite.__init__(self) # call sprite initializer
        self.frames = frames
        self.image = self.frames[0][0]
#        self.image = pygame.Surface([32, 32])
#        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.location = location
        self.lastLocation = location

        ## Translate to initial screen pixel position
        self.rect.x, self.rect.y = worldToScreen(self.location)

        self.direction = direction
        self.world = world
        self.speed = speed
        self.speeds = [ (0,-1* self.speed[1]),      #up
                       (self.speed[0], 0),      #right
                       (0, self.speed[1]),       #down
                       (-1* self.speed[0], 0) ]      # left 
        self.moveTarget = None
        self.distanceTraveled = 0
        self.alive = True
        self.add(self.world.sprites, self.world.movers)

    def getLocation(self):
        return self.location

    def setLocation(self, location):
        self.location = location

    def getLastLocation(self):
        return self.lastLocation

    def setLastLocation(self, location):
        self.lastLocation = location

    def updateLocation(self):
        location = screenToWorld(self.rect.center)   #[self.rect.center[0]/GRIDWIDTH, self.rect.center[1]/GRIDHEIGHT]
        self.location = location
        self.world.level[location[1]][location[0]] = self

        lastLoc = self.lastLocation
        level = self.world.level
        if location != lastLoc:
            level[lastLoc[1]][lastLoc[0]] = None
            self.lastLocation = location

#            print "[Debug]: ", lastLocation, " changed to", location
#            pass

    ### Update the agent every tick. Primarily does movement
    def update(self, delta):
        Thing.update(self, delta)
        if self.isMoving():
#           drawCross(self.world.background, self.moveTarget, (0, 0, 0), 5)
            # Figure out moveTarget's screen location
            target = worldToScreen(self.moveTarget)
            dx, dy = self.speeds[DIRECTION[self.direction]]            
#            print "delta= ", delta
            self.rect = self.rect.move(dx, dy)
            if (self.direction == 'up' and self.rect.y < target[1]) or (self.direction == 'right' and self.rect.x > target[0]) or (self.direction == 'down' and self.rect.y > target[1]) or (self.direction == 'left' and self.rect.x < target[0]):
                self.rect.x, self.rect.y = target
                self.distanceTraveled = self.distanceTraveled + 1
                self.stopMoving()                                            
            self.updateLocation()



### tells the mover to move one step in the specified direction
    def moveOneStep(self, direction):
        if self.isMoving():
            return None
        
        self.direction = direction
        target  = getLocation(self.location, direction, 1)        
        if locationValid(target, self.world.dimension):
            self.moveTarget = target
                
### tells the mover to move in the specified direction
    def move(self, direction):
        if self.isMoving():
            self.stopMoving()        
        self.direction = direction
        x, y = self.location
        if direction  == 'up':
            self.moveTarget = (x, 0)
        elif direction  == 'down':
            self.moveTarget = (x, self.world.dimension[1] - 1)
        elif direction  == 'left':
            self.moveTarget = (0, y)
        elif direction  == 'right':
            self.moveTarget = (self.world.dimension[0] - 1, y)
                


    def stopMoving(self):
        self.moveTarget = None
        self.snapToGrid()

    def snapToGrid(self):
        self.rect.x, self.rect.y = worldToScreen(self.location)
#        print "location = ", location, " | rect = ", worldToScreen(location)
        

    def isMoving(self):
        if self.moveTarget is not None:
            return True
        else:
            return False

    def getMoveTarget(self):
        return self.moveTarget
    
    ### When something collides with me
    def collision(self, thing):
        Thing.collision(self, thing)

        if self.isMoving():
            if isinstance(thing, Mover):
                self.stopMoving()
            elif isinstance(thing, GameWorld):
                self.stopMoving()
                
#       print "collision", self, thing
        return None

    def isAlive(self):
        return self.alive

    def die(self):
        self.alive = False
        self.world.level[self.location[1]][self.location[0]] = None
        self.remove(self.world.sprites, self.world.movers)




class Block(Mover):

    ### damage: amount of damage


    def __init__(self, world, location, direction = None,  frames = None,
                 speed = (BlockSpeed, BlockSpeed), health = BlockHealth, damage = BlockDamage):
        Mover.__init__(self, location, direction, speed, frames, world)
        self.health = health
        self.damage = damage
        self.add(self.world.blocks)


    def getHealth(self):
         return self.health

    def setHealth(self, health):
         self.health = health

    def getDamage(self):
        return self.damage

    ### Update the agent every tick. Primarily does movement
    def update(self, delta):
        Mover.update(self, delta)



    def collision(self, thing):       
        if self.isMoving(): 
            if isinstance(thing, Snobee):
                self.giveDamage(thing)
                if thing.alive:                   
                    if thing.state == 'hunt':
                        self.world.maxHunters -= 1
                        #print "hunters = ", self.world.maxHunters
                    thing.state = 'stunned'
                    Mover.collision(self, thing)
            else:
                Mover.collision(self, thing)
             
            
    def takeDamage(self, amount):
        self.health = self.health - amount
        ### Something should happen when hitpoints are <= 0
        if self.health < 0 and self.alive is True:
            self.die()

    def giveDamage(self, thing):
        if isinstance(thing, Block) or isinstance(thing, Creature):
            thing.takeDamage(self.damage)

    def die(self):
        Mover.die(self)
        self.remove(self.world.blocks)
        self.world.deleteBlock(self)


###########################
### Super class for Pengo and Sno-bee

class Creature(Mover):

    ### moveTarget: where to move to. Setting this to non-None value activates movement (update fn)
    ### moveOrigin: where moving from.
    ### navigator: model that does pathplanning
    ### firerate: how often agent can fire
    ### firetimer: how long since last firing
    ### canfire: can the agent fire?
    ### hitpoints: amount of damage the agent can take
    ### team: symbol referring to the team (or None)
    ### distanceTraveled: the total amount of distance traveled by the agent

    ### Constructor
    def __init__(self, world, location, direction, speed, frames,
        health, firerate, damage):
        Mover.__init__(self, location, direction, speed, frames, world)
        self.firerate = firerate
        self.firetimer = 0
        self.canfire = True
        self.health = health
        self.damage = damage
        self.navigator = None
        self.add(self.world.creatures)

    
        
    ### Update the agent every tick. Primarily does movement
    def update(self, delta):
        Mover.update(self, delta)
            
        if self.canfire == False:
            self.firetimer = self.firetimer + delta
            if self.firetimer >= self.firerate:
                self.canfire = True
                self.firetimer = 0
        return None

    def setNavigator(self, navigator):
        self.navigator = navigator
        navigator.setAgent(self)

    def navigateTo(self, dest):
        if self.navigator != None and locationValid(dest, self.world.dimension):
            self.navigator.computePath(self.location, dest)
            #print "compute path"

    def update(self, delta):        
        if self.navigator != None:
            path = self.navigator.path
            if path != None and self.isMoving() is False:
                if len(path) == 0:
                    self.navigator.path = None
                else:
                    loc = getLocation(self.location, path[0], 1)
                    if locationValid(loc, self.world.dimension):
                        thing = self.world.level[loc[1]][loc[0]]
                        if thing == None:
                            direction = path.pop(0)
                            self.moveOneStep(direction)
                            #print "direction = ", direction
                        
        Mover.update(self, delta)

        if self.canfire == False:
            self.firetimer = self.firetimer + delta
            if self.firetimer >= self.firerate:
                self.canfire = True
                self.firetimer = 0
                
        return None

        
                


### NOTE: problem: Agent can be subclassed and collision() can be overridden such that the agent is not stopped by obstacles/blockers
    def collision(self, thing):
        Mover.collision(self, thing)
        return None

    def place(self):
        location = getLocation(self.location, self.direction, 1)
        locValid = locationValid(location, self.world.dimension)
        if locValid is True and self.world.level[location[1]][location[0]] is None:
            block = Block(location, None, [10,10], 3, 100,
                          load_tile_table("stoneBlock.png"), self.world) 
            self.world.level[location[1]][location[0]] = block
            print "add block at ", location

    def take(self):
        location = getLocation(self.location, self.direction, 1)
        locValid = locationValid(location, self.world.dimension)
        if locValid is True and self.world.level[location[1]][location[0]] is not None:
            self.world.level[location[1]][location[0]].die()
            print "take block at ", location
            


### fire: push or crush
    def fire(self):
        if self.canfire:
            self.canfire = False
            location1 = getLocation(self.location, self.direction, 1)
            location2 = getLocation(self.location, self.direction, 2)

            loc1Valid = locationValid(location1, self.world.dimension)
            loc2Valid = locationValid(location2, self.world.dimension)

            if loc1Valid:
                thing1 = self.world.level[location1[1]][location1[0]]
                if isinstance(thing1, Block):
                    if loc2Valid is False:
                        thing1.takeDamage(self.damage)
                    elif loc2Valid is True:
                        thing2 = self.world.level[location2[1]][location2[0]]
                        if isinstance(thing2, Block):
                            thing1.takeDamage(self.damage)
                        else:
                            thing1.move(self.direction)
                    
#            for block in self.world.blocks:
#                if location1 == block.location:
#                    block.move(self.direction)            

    def takeDamage(self, amount):
        self.health = self.health - amount
        ### Something should happen when hitpoints are <= 0
        if self.health < 0 and self.alive is True:
            #print "die"
            self.die()

    def giveDamage(self, thing):
        if isinstance(thing, Block) or isinstance(thing, Creature):
            thing.takeDamage(self.damage)

    def die(self):
        Mover.die(self)
        self.remove(self.world.creatures)

############################
#Pengo
class  Pengo(Creature):
    def __init__(self, world, location, direction = 'right', speed = (PengoSpeed,PengoSpeed), frames = None,
        health = PengoHealth, firerate = PushRate, damage = PengoDamage):
        Creature.__init__(self, world, location, direction, speed, frames, health, firerate, damage)
        self.world.pengo = self


    def update(self, delta):
        Creature.update(self, delta)
        self.image = self.frames[DIRECTION[self.direction]][0]

    def die(self):
        Creature.die(self)
        self.world.pengo = None
        self.world.deletePengo(self)

    def collision(self, thing):
        if isinstance(thing, Snobee):
            if thing.state == 'stunned':
                thing.takeDamage(10000)
        else:           
            Creature.collision(self, thing)
    

############################
# Sno-bee
class Snobee(Creature):
    def __init__(self, world, location, direction = 'right', speed = (SnobeeSpeed,SnobeeSpeed), frames = None,
        health = SnobeeHealth, firerate = AttackRate, damage = SnobeeDamage):
        self.state = 'wander'   #other states include 'hunt' and 'stunned'
        self.huntTimer = 0
        self.stunTimer = 0
        self.planExpireTimer = 0
        Creature.__init__(self, world, location, direction, speed, frames, health, firerate, damage)
        Creature.setNavigator(self, GreedyGridNavigator())
        self.add(self.world.snobees)

    def attackFront(self):
        if self.canfire is False:
            return None

        self.canfire = False    
        location = getLocation(self.location, self.direction, 1)
        locValid = locationValid(location, self.world.dimension)
        if locValid is True:
            thing = self.world.level[location[1]][location[0]]
            if thing is not None:
                self.giveDamage(thing) 
                #print "attacking ", location, "damage = ", self.damage
                
    def attack(self, thing):
        if self.canfire is False:
            return None

        self.canfire = False 
        self.giveDamage(thing) 

    def pengoDistance(self):
        current = self.location
        destination = self.world.pengo.location
        return math.fabs(current[0] - destination[0]) + math.fabs(current[1] - destination[1]) #distance(self.location, self.world.pengo.location)
        
    def update(self, delta):
        self.stateMachine(delta)

        if self.state == 'stunned':
            return None
        
        Creature.update(self, delta)
        self.planExpireTimer = self.planExpireTimer + delta
        if self.navigator != None and self.planExpireTimer > ReplanTime:
            self.navigator.path = None
            self.planExpireTimer = 0
            
        if self.navigator != None and self.navigator.path == None:
            if self.state == 'hunt' and self.world.pengo != None: #and self.world.maxHunters < 2:                
                dx = self.world.pengo.location[0] #random.randint(0, self.world.dimension[0] - 1)
                dy = self.world.pengo.location[1] #random.randint(0, self.world.dimension[1] - 1)                
            elif self.state == 'wander':
                dx = random.randint(0, self.world.dimension[0] - 1)
                dy = random.randint(0, self.world.dimension[1] - 1)

            self.navigateTo((dx, dy))               
            #print "Navigate to: ", (dx, dy)

        if self.navigator != None:
            path = self.navigator.path
            if path != None and self.isMoving() is False:
                if len(path) > 0:
                    loc = getLocation(self.location, path[0], 1)
                    if locationValid(loc, self.world.dimension):
                        thing = self.world.level[loc[1]][loc[0]]
                        if thing != None:
                            if (isinstance(thing, Block) and thing.health < 100) or isinstance(thing, Pengo):
                                self.attack(thing)
                            #elif isinstance(thing, Snobee):
                                #self.navigator.path = None
                                #self.planExpireTimer = 0
                            
    def stateMachine(self, delta):
        if self.state == 'wander' and  self.world.maxHunters < 2:
            if self.world.pengo != None and (self.pengoDistance() < HuntDistance):
                self.state = 'hunt'
                self.world.maxHunters += 1
                #print "hunting begin: ",  self.world.maxHunters
        
        if self.state == 'hunt':
            self.huntTimer = self.huntTimer + delta
            #if self.huntTimer >= HuntDuration:
                #print "hunt timer reset ", self.huntTimer           

        if self.state == 'hunt' and self.huntTimer > HuntDuration:
            self.state = 'wander'
            self.world.maxHunters -= 1
            self.huntTimer = 0           
            #print "stop hunting", self.world.maxHunters

        if self.state == 'stunned':
            self.stunTimer = self.stunTimer + delta
            
        if self.state == 'stunned' and self.stunTimer > StunDuration:
            self.state = 'wander'
            self.stunTimer = 0
            

        
        
    def collision(self, thing):
        if isinstance(thing, Snobee):
            return None      

        if self.state != 'stunned':
            if isinstance(thing, Pengo): 
                    self.attack(thing)
            elif isinstance(thing, Block):
                if thing.isMoving() is False:
                    self.attack(thing)
            
        Creature.collision(self, thing)
                
            

    def die(self):
        Creature.die(self)
        if self.state == 'hunt':
            self.world.maxHunters -= 1
            #print "stop hunting", self.world.maxHunters
        self.remove(self.world.snobees)
        self.world.deleteSnobee(self)
        #print "Total Kills: ", self.world.kill
        #print "die"

############################
### GameWorld

class GameWorld():

    ### screen: the screen
    ### background: the background surface
    ### agent: the player agent
    ### obstacles: obstacles
    ### sprites: all sprites (player and NPCs)
    ### npcs: the NPC agents
    ### dimensions: the size of the world (width, height)
    ### points: all the points of obstacles, plus screen corners
    ### lines: all the points of obstacles, plus screen edges
    ### bullets: all the bullets active
    ### resources: all the resources
    ### movers: all things that can collide with other things and implement collision()
    ### destinations: places that are not inside of obstacles. 
    ### clock: elapsed time in game

    def __init__(self, seed = 0):
        #initialize random seed
        self.time = time.time()
        corerandom.seed(seed or self.time)
        random.seed(self.time)
        #initialize pygame and set up screen and background surface
        pygame.init()
        screen = pygame.display.set_mode(SCREENSIZE)
#        pygame.display.init()
        pygame.display.set_caption('Pengo Remake')
        #pygame.mouse.set_visible(0)
        # Background surface that will hold everything
#        background = pygame.Surface(screen.get_size())
        background = pygame.Surface(SCREENSIZE)
        background = background.convert()
        background.fill(GREEN)
        #store stuff
        self.screen = screen
        self.seed = seed or self.time
        self.background = background       
        self.font = pygame.font.SysFont(None, 20, False, False)
        self.done = False
        #the following need to reset when a new game begins
        self.sprites = pygame.sprite.Group()
        self.movers = pygame.sprite.Group()
        self.snobees = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.creatures = pygame.sprite.Group()
        self.pengo = None
        self.maxHunters = 0
        self.kills = 0
        self.lives = 0
        self.mosters = MaxMonsters
        self.clock = 0
        self.dimension = None 
        self.level = None 
        
#        print self.level


    def reset(self):
        self.sprites.empty()
        self.movers.empty()
        self.snobees.empty()
        self.blocks.empty()
        self.creatures.empty()
        self.pengo = None
        self.maxHunters = 0
        self.kills = 0
        self.mosters = MaxMonsters
        self.lives = 0
        self.clock = 0
        self.dimension = None 
        self.level = None
        


        
    def loadLevel(self):
 #       grass = pygame.image.load("leavesBlock.png").convert()
 #       iceDirtBlock = pygame.image.load("iceDirtBlock.png").convert()
        
        dict = {"X": "stoneBlock.png", "C": "coin.png"}
        self.dimension = (LEVELWIDTH, LEVELHEIGHT)
        self.level =  [ [None] * LEVELWIDTH  for i in range(LEVELHEIGHT)]
        for i in range(LEVELHEIGHT):
            for j in range(LEVELWIDTH):
                if LEVEL[i][j] == '.':
#                    self.sprites.add(Tile([j,i], grass))
                    continue
                if LEVEL[i][j] == 'X':
                    health = BlockHealth
                elif LEVEL[i][j] == 'C':
                    health = 1000000
                block = Block(self, (j,i), frames = load_tile_table(dict[LEVEL[i][j]]), health = health)
                self.level[i][j] = block

        

    

    def setPlayer(self, x, y):
        self.lives += 1
        self.pengo = Pengo(self, (x, y), frames = load_tile_table("player.png"))
        self.level[y][x] = self.pengo


    def spawnSnobee(self, x, y):
        self.mosters -= 1
        snobee = Snobee(self, (x, y), frames = load_tile_table("blobLeft.png"))
        self.level[y][x] = snobee
        


    def run(self):
#        self.sprites = pygame.sprite.RenderPlain((self.pengo))
#        for r in self.resources:
#            self.sprites.add(r)
#        for n in self.npcs:
#            self.sprites.add(n)
#        for m in self.movers:
#            self.sprites.add(m)
        clock = pygame.time.Clock()
        

        while not self.done:                
            clock.tick(TICK)
            pygame.display.set_caption("fps: " + str(clock.get_fps()))
            delta = clock.get_time()
            self.handleEvents()
            self.update(delta)
            self.drawWorld()
            pygame.display.flip()
            
        pygame.quit()


    def handleEvents(self): 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

        # Set the speed based on the key pressed
            elif event.type == pygame.KEYDOWN:
                if self.pengo == None:
                    return None
                
                if event.key == pygame.K_a:
                    self.pengo.move('left')
                elif event.key == pygame.K_d:
                    self.pengo.move('right')
                elif event.key == pygame.K_w:
                    self.pengo.move('up')
                elif event.key == pygame.K_s:
                    self.pengo.move('down')
                elif event.key == pygame.K_RETURN:
                    self.pengo.fire()
                #elif event.key == pygame.K_LCTRL:
                    #self.pengo.place() 
                #elif event.key == pygame.K_LALT:
                    #self.pengo.take()
                

            # Reset speed when key goes up
            elif event.type == pygame.KEYUP:
                if self.pengo == None:
                    return None
                
                if event.key == pygame.K_a and self.pengo.direction == 'left':
                    self.pengo.stopMoving()
                elif event.key == pygame.K_w and self.pengo.direction == 'up':
                    self.pengo.stopMoving()
                elif event.key == pygame.K_d and self.pengo.direction == 'right':
                    self.pengo.stopMoving()
                elif event.key == pygame.K_s and self.pengo.direction == 'down':
                    self.pengo.stopMoving()

                 


                
    def update(self, delta):
        self.sprites.update(delta)                             
        self.worldCollisionTest()
        self.clock = self.clock + delta

        return None

    def worldCollisionTest(self):
        # Collision against world boundaries
        for m1 in self.movers:
            if m1.rect.center[0] < 0 or m1.rect.center[0] > SCREENSIZE[0] or m1.rect.center[1] < 0 or m1.rect.center[1] > SCREENSIZE[1]:
                m1.collision(self)
                self.collision(m1)
        # Movers against movers
        hit_dict = pygame.sprite.groupcollide(self.movers, self.movers, False, False, collided = None)
        for m1 in hit_dict:
            for m2 in hit_dict[m1]:
                if m1 != m2:
                    m1.collision(m2)



    def drawWorld(self):
        self.screen.blit(self.background, (0,0))
#        self.pengos.draw(self.screen)
#        self.blocks.draw(self.screen)
        self.sprites.draw(self.screen)

        #draw texts
        self.drawTexts(self.font, "Monsters: " + str(MaxMonsters - self.kills), [5,5], BLACK)
        self.drawTexts(self.font, "Kills: " + str(self.kills), [5,20], BLACK)
        self.drawTexts(self.font, "Lives: " + str(MaxLives - self.lives), [5,35], BLACK)
        

    def drawTexts(self, font, text, pos, color):
        text = font.render(text, True, color)
        self.screen.blit(text, pos)       
        

    def collision(self, thing):
        return None

    def deleteBlock(self, block):
        pass
                

    def deleteSnobee(self, snobee):
        self.kills += 1
        if self.mosters > 0:
            loc = random.choice([(1,1), (1,18), (18,1), (18, 18)])
            self.spawnSnobee(loc[0], loc[1])
        
        if self.snobees.sprites() == []:
            font = pygame.font.SysFont(None, 30, True, False)
            self.drawTexts(font, "Monsters: " + str(MaxMonsters - self.kills), [280,150], BLACK)
            self.drawTexts(font, "Kills     : " + str(self.kills), [280,200], BLACK)
            self.drawTexts(font, "Lives     : " + str(MaxLives - self.lives), [280,250], BLACK)
            font = pygame.font.SysFont(None, 60, True, True)
            self.drawTexts(font, "You win!", [250, 300], [200, 0, 0])
            pygame.display.flip()
            pygame.time.wait(3000)
            self.reset()
            self.init()
            
            
        

    def deletePengo(self, pengo):       
        if self.lives < MaxLives:
            thing = self.level[10][10]
            if thing != None:
                if isinstance(thing, Block) or isinstance(thing, Snobee):
                    thing.die()               
            self.setPlayer(10, 10)
        else:
            font = pygame.font.SysFont(None, 30, True, False)
            self.drawTexts(font, "Monsters: " + str(MaxMonsters - self.kills), [280,150], BLACK)
            self.drawTexts(font, "Kills     : " + str(self.kills), [280,200], BLACK)
            self.drawTexts(font, "Lives     : " + str(MaxLives - self.lives), [280,250], BLACK)
            font = pygame.font.SysFont(None, 60, True, True)
            self.drawTexts(font, "You lose!", [250, 300], [200, 0, 0])
            pygame.display.flip()
            pygame.time.wait(3000)
            self.reset()
            self.init()

    def init(self):
        self.loadLevel()
        self.setPlayer(10, 10)
        self.spawnSnobee(1, 1)
        self.spawnSnobee(18, 1)
        self.spawnSnobee(1, 18)
        self.spawnSnobee(18, 18)

    
  
            

world = GameWorld()
world.init()
world.run()


