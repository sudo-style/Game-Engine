import pygame
from pygame.locals import *
import os
import math
from random import randint

from Item import Item, Explosive
from Character import Character, Player, NPC
from GameObject import GameObject

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
        self.addExplosive((width/2, height/2))
        self.addCharacter((width/2, height/2), 'clown')
        self.addItem((width/2-200, height/2+ 100), 'gun', 5)
        self.addEnemy((width, height/2), 'guard')
    
    def addExplosive(self, pos, name = 'bomb'):
        explosive = Explosive(pos, self.camera_group, self, name)
        self.items.append(explosive)

    def addItem(self, pos, name, n = 1):
        item = Item(pos, self.camera_group, self, name, n)
        self.items.append(item)

    def addCharacter(self, pos, name):
        character = Character(pos, self.camera_group, self, name)
        self.npcs.append(character)

    def addEnemy(self, pos, name):
        character = NPC(pos, self.camera_group, self, name)
        self.npcs.append(character)