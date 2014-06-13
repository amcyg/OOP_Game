import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import random

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

    def interact(self):
        PLAYER.inventory[self.NAME] = PLAYER.inventory.get(self.NAME, []) + [self]
        GAME_BOARD.draw_msg("You just acquired a %s! You have %d %s(s)! " % \
        (self.NAME, len(PLAYER.inventory[self.NAME]), self.NAME) )
        
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

class Heart(GameElement):
    IMAGE = "Heart"
    SOLID = True

class Cat(GameElement):
    IMAGE = "Cat"
    SOLID = True

    def interact(self):
        msg = ""
        print "The player has this stuff: ", itemize(PLAYER.inventory)
        for name, num in winning_combo.iteritems():
            items = PLAYER.inventory.get(name, False)
            if items:
                if  len(items) > num:
                    msg = "Grumpy Cat says: Pshh. Too many %ss." % name
                    break
                if len(items) < num:
                    msg = "Grumpy Cat says: Meh. Bring me more %ss." % name
                    break
            else:
                msg = "Grumpy Cat says: Hmph...you don't even have any %ss." % name
                break
        else:
            msg = "Grumpy Cat says: I guess that's ok."
            x_cat = self.x
            y_cat = self.y
            heart = Heart()
            GAME_BOARD.register(heart)
            GAME_BOARD.set_el(x_cat, y_cat, heart)
        GAME_BOARD.draw_msg(msg)
        

class ShortTree(GameElement):
    IMAGE = "ShortTree"
    SOLID = True

class TallTree(GameElement):
    IMAGE = "TallTree"
    SOLID = True



def gen_world():
    world = {}
    coords = [(x,y) for x in range(10) for y in range(10)]

    num_obstacles = random.randint(5, 9)
    for i in range(num_obstacles):
        c = random.choice(coords)
        o = random.choice([Rock, ShortTree, TallTree])
        world[c] = o
        coords.remove(c)

    num_gems = 15
    gem_dict = {}
    for i in range(num_gems):
        c = random.choice(coords)
        g = random.choice([BlueGem, OrangeGem, GreenGem])
        world[c] = g
        gem_dict[g.NAME] = gem_dict.get(g.NAME, 0) + 1
        coords.remove(c)
    print "Distribution of gems on the board: ", gem_dict

    global winning_combo
    winning_combo = {}
    for name, num in gem_dict.iteritems():
        rand_num = random.randint(1, num)
        winning_combo[name] = rand_num
    print "Winning combo: ", winning_combo

    c1 = random.choice(coords)
    world[c1] = Cat
    coords.remove(c1)

    global PLAYER
    c2 = random.choice(coords)
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(c2[0], c2[1], PLAYER)

    return world


def initialize():
    """Put game initialization code here"""
    global LEVEL_1
    LEVEL_1 = gen_world()

    for coord, kind in LEVEL_1.iteritems():
        item = kind()
        GAME_BOARD.register(item)
        GAME_BOARD.set_el(coord[0], coord[1], item)

    GAME_BOARD.draw_msg("This game is wicked awesome. ")


def in_boundary(x, y):
    if x < 0 or x > (GAME_WIDTH - 1):
        return False
    if y < 0 or y > (GAME_HEIGHT - 1):
        return False
    return True

def check_drop(object):
    # check to see if there's room for the dropped item
    potential_x = PLAYER.x - 1
    obstacle = GAME_BOARD.get_el(potential_x, PLAYER.y)
    if obstacle is None and in_boundary(potential_x, PLAYER.y):
        GAME_BOARD.set_el(potential_x, PLAYER.y, object)
        return True
    return False


def drop(key):
    items = PLAYER.inventory.get(key, [])
    if len(items):
        if check_drop(items[-1]):
            items.pop()
            msg =  "Dropped a %s." % key
        else:
            msg = "Could not drop %s." % key
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
        num_list = [n for n in range(1, len(PLAYER.inventory) + 1)]
        key_mapping = zip(num_list, PLAYER.inventory)

        msg = ["Choose your operation:"]
        for num, item in key_mapping:
            msg.append("Press %d to drop a %s." % (num, item))
        msg.append("Press N to cancel.")
        GAME_BOARD.draw_msg(' '.join(msg))
        global K_STATE
        K_STATE = key_mapping

    if KEYBOARD[key.N]:
        GAME_BOARD.draw_msg("Alright, nevermind. ")
        global K_STATE
        K_STATE = 0

def alt_key_2():
    global K_STATE

    for num, item in K_STATE:
        attr = '_%d' % num
        if KEYBOARD[getattr(key, attr)]:
            msg = drop(item)
            GAME_BOARD.draw_msg(msg)
            K_STATE = 0
        if KEYBOARD[key.N]:
            GAME_BOARD.draw_msg("Alright, nevermind.")
            K_STATE = 0

def keyboard_handler():
    global K_STATE
    if K_STATE == 0:
        standard_keyboard()
    if K_STATE == 1:
        alt_key_1()  
    if type(K_STATE) == list:
        alt_key_2()           

def interact(x, y, obstacle):
    if obstacle:
        obstacle.interact()

def move(x, y, obstacle):
    if  obstacle is None or not obstacle.SOLID:
        GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        GAME_BOARD.set_el(x, y, PLAYER)







