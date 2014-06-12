import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
K_STATE = 0
######################

GAME_WIDTH = 10
GAME_HEIGHT = 10

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Character(GameElement):
    IMAGE = "Horns"

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = {}

class Gem(GameElement):
    SOLID = False
    COLOR = "no color"
    TYPE = "gem"

    def interact(self, player):
        player.inventory[self.NAME] = player.inventory.get(self.NAME, []) + [self]
        # player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a %s! You have %d items! " % (self.NAME, len(player.inventory)))
        
class BlueGem(Gem):
    IMAGE = "BlueGem"
    COLOR = "blue"
    NAME = "blue gem"

class GreenGem(Gem):
    IMAGE = "GreenGem"
    COLOR = "green"
    NAME = "green gem"

class OrangeGem(Gem):
    IMAGE = "OrangeGem"
    COLOR = "orange"
    NAME = "orange gem"

class Block(GameElement):
    IMAGE = "Block"
    SOLID = True

class GrassBlock(Block):
    IMAGE = "GrassBlock"

class StoneBlock(Block):
    IMAGE = "StoneBlock"


####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    rock_positions = [
            (2,1),
            (1,2),
            (3,2),
            (2,3)
            ]
    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    rocks[-1].SOLID = False


    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)

    GAME_BOARD.draw_msg("This game is wicked awesome. ")

    gem1 = BlueGem()
    GAME_BOARD.register(gem1)
    GAME_BOARD.set_el(9 , 5, gem1)

    gem2 = GreenGem()
    GAME_BOARD.register(gem2)
    GAME_BOARD.set_el(9, 4, gem2)

    gem3 = OrangeGem()
    GAME_BOARD.register(gem3)
    GAME_BOARD.set_el(9, 7, gem3)

    gem4 = BlueGem()
    GAME_BOARD.register(gem4)
    GAME_BOARD.set_el(9 , 9, gem4)

def in_boundary(x, y):
    if x < 0 or x > (GAME_WIDTH - 1):
        return False
    if y < 0 or y > (GAME_HEIGHT - 1):
        return False
    return True

def drop(key):
    msg = ""
    inventory = PLAYER.inventory.get(key, [])
    if len(inventory):
        # drop the thing
        dropped = inventory.pop()
        msg = "You dropped a %s. You have %d %s(s) left. " % (dropped.NAME, len(inventory), dropped.NAME)
        print PLAYER.inventory
    else:
        msg = "Error: can't drop what you don't have! "
    return msg

def itemize(mydict):
    summary = []
    for k, v in mydict.iteritems():
        summary.append("%d %s(s)" % (len(v), k))
    summary = ", ".join(summary)

    msg = "You have: %s. " % summary

    return msg

def standard_keyboard():
    global K_STATE
    if KEYBOARD[key.D]:
        GAME_BOARD.draw_msg("Do you want to drop something? ")
        K_STATE = 1

    if KEYBOARD[key.I]:
        stuff = PLAYER.inventory
        GAME_BOARD.draw_msg(itemize(stuff))
        
    direction = None
    if KEYBOARD[key.UP]:
        direction = "up"
    if KEYBOARD[key.DOWN]:
        direction = "down"
    if KEYBOARD[key.LEFT]:
        direction = "left"
    if KEYBOARD[key.RIGHT]:
        direction = "right"

    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        if in_boundary(next_x, next_y):

            existing_el = GAME_BOARD.get_el(next_x, next_y)

            interact(next_x, next_x, existing_el)

            move(next_x, next_y, existing_el)

def alt_key_1():
    if KEYBOARD[key.Y]:
        GAME_BOARD.draw_msg("Ok, let's do it. ")
        global K_STATE
        K_STATE = 2
    if KEYBOARD[key.N]:
        GAME_BOARD.draw_msg("Alright, nevermind. ")
        global K_STATE
        K_STATE = 0

def alt_key_2():
    # insert print statement to user to pick which one to drop

    #map items in inventory to strings '_1', '_2', etc.

    GAME_BOARD.draw_msg("Choose your operation: 1) Drop a blue gem. 2) Drop an orange gem. 3) Drop a green gem. Press 'N' to cancel.")
    global K_STATE

    mystr = "_1"

    if KEYBOARD[getattr(key, num)]:
        msg = drop(item)
        K_STATE = 3
    if KEYBOARD[key._2]:
        msg = drop("orange gem")
        K_STATE = 3
    if KEYBOARD[key._3]:
        msg = drop("green gem")
        K_STATE = 3
    if KEYBOARD[key.N]:
        GAME_BOARD.draw_msg("Alright, nevermind.")
        K_STATE = 0

def alt_key_3():
    # insert print statement confirming what was dropped
    global K_STATE
    GAME_BOARD.draw_msg(itemize(PLAYER.inventory) + "Do you want to drop anything else? (Y/N)")
    if KEYBOARD[key.Y]:
        K_STATE = 2
    if KEYBOARD[key.N]:
        GAME_BOARD.draw_msg("")
        K_STATE = 0

def keyboard_handler():
    global K_STATE
    if K_STATE == 0:
        standard_keyboard()
    if K_STATE == 1:
        alt_key_1()  
    if K_STATE == 2:
        alt_key_2()
    if K_STATE == 3:
        alt_key_3()             

def interact(x, y, obstacle):
    if obstacle:
        obstacle.interact(PLAYER)

def move(x, y, obstacle):
    if  obstacle is None or not obstacle.SOLID:
        GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        GAME_BOARD.set_el(x, y, PLAYER)







