# -*- coding: utf-8 -*-
"""
Spyder Editor

Constants """



# Constants

### Levels should be rectangles, not necessarily square. You can make your own level
### similarly. X represents a block, C represents an unbreakable coin (yellow ellipse),
### and . represent nothing.
LEVEL0 =    ['XXXXXXXXXXXXXXXXXXXX'
            ,'X............XX....X'
            ,'X...C..XX....XX....X'
            ,'X......XX..........X'
            ,'X.XXXXXXXXX..XXXXX.X'
            ,'X......XX....XX....X'
            ,'X......XX....XXXX..X'
            ,'X.........C...X....X'
            ,'X.XXXXXX......X....X'
            ,'X...C.XX......X....X'
            ,'X.....XX...........X'
            ,'X............XX....X'
            ,'X.XXXXXXXXX..XXXXX.X'
            ,'X......XX....XX....X'
            ,'X......XX....XXXX..X'
            ,'X.........C...X....X'
            ,'X.XXXXXX......X....X'
            ,'X...C.XX......X....X'
            ,'X.....XX...........X'
            ,'XXXXXXXXXXXXXXXXXXXX'
            ]

LEVEL =     ['XXXXXXXXXXXXXXXXXXXX'      # this level is loaded automatically
            ,'X.X....X.........X.X'
            ,'X.X.XXXX.XXXXXXC.X.X'
            ,'X.X......XX.....XX.X'
            ,'X.XXX.XXXXXX..XXXX.X'
            ,'X.X...........XX.X.X'
            ,'X...XXXXXXCXXXXX.X.X'
            ,'X.X.....X.X..XX..X.X'
            ,'X.XXXXX.X.X..XX..X.X'
            ,'X.X..XX.X.X..XX..X.X'
            ,'X.X..XX......XX....X'
            ,'X.X..XX.X.X.XXX..X.X'
            ,'X.X..XCXXXX..XX..X.X'
            ,'X....XX......XX..X.X'
            ,'X.X..XX......XX.XX.X'
            ,'X.X......XXXXXX..X.X'
            ,'X.X..XXX.....XX..X.X'
            ,'X.X..XCX..XXXCXX.X.X'
            ,'X.X..............X.X'
            ,'XXXXXXXXXXXXXXXXXXXX'
            ]

##### Do not change this block! #######################################################
LEVELWIDTH, LEVELHEIGHT = len(LEVEL[0]), len(LEVEL)  # world dimensions
GRIDWIDTH, GRIDHEIGHT = 32, 32 # pixel 
SCREENSIZE = [LEVELWIDTH * GRIDWIDTH, LEVELHEIGHT * GRIDHEIGHT] 

DIRECTION = {'up': 0, 'right': 1, 'down': 2, 'left': 3}
Directions = ['up', 'right', 'down', 'left']
#######################################################################################




#### Game Settings, feel free to change them ##################################
TICK = 60  #Max FPS

# Blocks
BlockHealth = 10
BlockSpeed = 12
BlockDamage = 100

# Snobees
SnobeeHealth = 1  # if a snobee's health is high enough, a moving block may just stun it, instead of killing it.
SnobeeSpeed = 4
SnobeeDamage = 1
AttackRate = 200   # 单位：毫秒
HuntDistance = 6
#HuntChance = 600
HuntDuration = 9000  # 单位：毫秒
StunDuration = 2000 #stunned duration by blocks
MaxMonsters = 30
ReplanTime = 2000  # 单位：毫秒 path finding frequence

# Pengo
MaxLives = 3
PengoHealth = 1
PengoSpeed = 5
PengoDamage = 100
PushRate = 200  # 单位：毫秒
#######################################################################################





# the following are  just color macros, not much to say
colors_hex = [
    0x000000,0x404040,0x6C6C6C,0x909090,0xB0B0B0,0xC8C8C8,0xDCDCDC,0xECECEC,
    0x444400,0x646410,0x848424,0xA0A034,0xB8B840,0xD0D050,0xE8E85C,0xFCFC68,
    0x702800,0x844414,0x985C28,0xAC783C,0xBC8C4C,0xCCA05C,0xDCB468,0xECC878,
    0x841800,0x983418,0xAC5030,0xC06848,0xD0805C,0xE09470,0xECA880,0xFCBC94,
    0x880000,0x9C2020,0xB03C3C,0xC05858,0xD07070,0xE08888,0xECA0A0,0xFCB4B4,
    0x78005C,0x8C2074,0xA03C88,0xB0589C,0xC070B0,0xD084C0,0xDC9CD0,0xECB0E0,
    0x480078,0x602090,0x783CA4,0x8C58B8,0xA070CC,0xB484DC,0xC49CEC,0xD4B0FC,
    0x140084,0x302098,0x4C3CAC,0x6858C0,0x7C70D0,0x9488E0,0xA8A0EC,0xBCB4FC,
    0x000088,0x1C209C,0x3840B0,0x505CC0,0x6874D0,0x7C8CE0,0x90A4EC,0xA4B8FC,
    0x00187C,0x1C3890,0x3854A8,0x5070BC,0x6888CC,0x7C9CDC,0x90B4EC,0xA4C8FC,
    0x002C5C,0x1C4C78,0x386890,0x5084AC,0x689CC0,0x7CB4D4,0x90CCE8,0xA4E0FC,
    0x003C2C,0x1C5C48,0x387C64,0x509C80,0x68B494,0x7CD0AC,0x90E4C0,0xA4FCD4,
    0x003C00,0x205C20,0x407C40,0x5C9C5C,0x74B474,0x8CD08C,0xA4E4A4,0xB8FCB8,
    0x143800,0x345C1C,0x507C38,0x6C9850,0x84B468,0x9CCC7C,0xB4E490,0xC8FCA4,
    0x2C3000,0x4C501C,0x687034,0x848C4C,0x9CA864,0xB4C078,0xCCD488,0xE0EC9C,
    0x442800,0x644818,0x846830,0xA08444,0xB89C58,0xD0B46C,0xE8CC7C,0xFCE08C]


black = colors_hex[0]
white = colors_hex[7]
green = colors_hex[90]
red = colors_hex[33]
blue = colors_hex[65]
yellow = colors_hex[15]
cyan = colors_hex[60]
magenta = colors_hex[46]
grey = colors_hex[1]

GREEN = colors_hex[20]
RED = [255, 0, 0]
BLACK = [  0,   0,   0]
WHITE = [255, 255, 255]
