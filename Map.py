import pygame
from pygame.locals import *
import os
import math
from random import randint

from Item import Item, Explosive
from Character import Character, Player

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
playerKeys = [K_LEFT, K_RIGHT, K_UP, K_DOWN]

class Map:
    def __init__(self, name, width, height, screen, clock, fps, camera_group):
        self.name = name
        self.descritpion = ""
        self.targets = []
        self.rooms = []
        self.items = []
        self.npcs = []
        self.original_sprite = pygame.image.load(os.path.join("sprites", 'map', "GroundFloor.png"))
        self.sprite = self.original_sprite.copy()
        
        self.width = width
        self.height = height
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.camera_group = camera_group

        # add player to the map
        self.player = Player((width/2, height/2), self.camera_group, self, 'player')
        
        # adding an npc to the map
        self.addNPC((width, height/2), 'clown')

        # adding an item to the map
        #self.addItem((width/2, height/2), 'camera')

        self.addExplosive((width/2, height/2))
        self.addNPC((width/2, height/2), 'clown')
    
    def addExplosive(self, pos, name = 'bomb'):
        explosive = Explosive(pos, self.camera_group, self, name)
        self.items.append(explosive)

    def addItem(self, pos, name):
        item = Item(pos, self.camera_group, self, name)
        self.items.append(item)

    def addNPC(self, pos, name):
        character = Character(pos, self.camera_group, self, name)
        self.npcs.append(character)