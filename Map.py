import pygame
from pygame.locals import *
import os
import math
from random import randint

from Item import Item, Explosive, Food
from Character import Character, Player, NPC, Guard
from GameObject import GameObject


class Map:
    def __init__(self, name, width, height, screen, clock, fps, camera_group):
        self.name = name
        self.descritpion = ""
        self.targets, self.rooms, self.items, self.npcs, self.foods = [], [], [], [], []
        self.original_sprite = pygame.image.load(os.path.join("sprites", 'map', "GroundFloor.png"))
        self.sprite = self.original_sprite.copy()
        
        self.width = width
        self.height = height
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.camera_group = camera_group

        # adding food to the map
        self.addFood((200,500), 'apple')

        # add player to the map
        self.player = Player((width/2, height/2), self.camera_group, self, 'player')
        
        # adding an npc to the map
        self.addExplosive((width/2, height/2))
        self.addItem((width/2-200, height/2+ 100), 'gun', 5)
        self.addNPC((width/2, height/2), 'clown')
        self.addGuard((width, height/2), 'guard')
        self.addGuard((width/2 + 200, height/2 + 200), 'guard')
    
    def addExplosive(self, pos, name = 'bomb'):
        explosive = Explosive(pos, self.camera_group, self, name)
        self.items.append(explosive)

    def addItem(self, pos, name, count = 1):
        item = Item(pos, self.camera_group, self, name, count)
        self.items.append(item)

    def addNPC(self, pos, name):
        npc = NPC(pos, self.camera_group, self, name)
        self.npcs.append(npc)

    def addGuard(self, pos, name):
        guard = Guard(pos, self.camera_group, self, name)
        self.npcs.append(guard)

    def addFood(self, pos, name):
        food = Food(pos, self.camera_group, self, name)
        self.foods.append(food)