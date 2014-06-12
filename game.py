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
        self.inventory = []

class Gem(GameElement):
    SOLID = False
    COLOR = "no color"
    TYPE = "gem"

    def interact(self, player):

        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a %s gem! You have %d items!" % (self.COLOR, len(player.inventory)))
        
class BlueGem(Gem):
    IMAGE = "BlueGem"
    COLOR = "blue"

class GreenGem(Gem):
    IMAGE = "GreenGem"
    COLOR = "green"

class OrangeGem(Gem):
    IMAGE = "OrangeGem"
    COLOR = "orange"

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

    GAME_BOARD.draw_msg("This game is wicked awesome.")

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

def drop(color):
    for item in PLAYER.inventory:
        if item.COLOR == color:
            PLAYER.inventory.remove(item)



def itemize(mylist):
    mydict = {}
    summary = []
    for item in mylist:
        description = item.COLOR + ' ' + item.TYPE
        mydict[description] = mydict.get(description, 0) + 1
    for entry in mydict:
        summary.append("%d %s(s)" % (mydict[entry], entry))

    summary = ", ".join(summary)
    GAME_BOARD.draw_msg("You have: %s." % summary)


def standard_keyboard():
    global K_STATE
    if KEYBOARD[key.D]:
        GAME_BOARD.draw_msg("Do you want to drop something?")
        K_STATE = 1

    if KEYBOARD[key.I]:
        stuff = PLAYER.inventory
        itemize(stuff)
        
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
        GAME_BOARD.draw_msg("Ok, let's do it.")
        global K_STATE
        K_STATE = 2
    if KEYBOARD[key.N]:
        GAME_BOARD.draw_msg("Alright, nevermind.")
        global K_STATE
        K_STATE = 0

def alt_key_2():
    itemize(PLAYER.inventory)
    # insert print statement to user to pick which one to drop
    GAME_BOARD.draw_msg("Choose your operation: \n 1) Drop a blue gem. \n 2) Drop an orange gem. \n 3) Drop a green gem. \n Press 'N' to cancel.")

    if KEYBOARD[key._1]:
        drop("blue")
        GAME_BOARD.draw_msg("You have %d blue gems left.") 
    if KEYBOARD[key._2]:
        drop("orange")
    if KEYBOARD[key._3]:
        drop("green")
    if KEYBOARD[key.N]:
        GAME_BOARD.draw_msg("Alright, nevermind.")
        global K_STATE
        K_STATE = 0




def keyboard_handler():
    global K_STATE
    if K_STATE == 0:
        standard_keyboard()
    if K_STATE == 1:
        alt_key_1()  
    if K_STATE == 2:
        alt_key_2()             

def interact(x, y, obstacle):
    if obstacle:
        obstacle.interact(PLAYER)

def move(x, y, obstacle):
    if  obstacle is None or not obstacle.SOLID:
        GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        GAME_BOARD.set_el(x, y, PLAYER)







