import pygame
from pygame.locals import *
import os
import math
from random import randint

from Item import Item
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
        self.original_sprite = pygame.image.load(os.path.join("sprites", "GroundFloor.png"))
        self.sprite = self.original_sprite.copy()
        
        self.width = width
        self.height = height
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.camera_group = camera_group

        self.player = Player((width/2, height/2), self.camera_group, self, 'player')
        
        # adding an npc to the map
        self.npcs.append(Character((0,0), self.camera_group, self, 'clown'))
        self.npcs.append(Character((width,0), self.camera_group, self, 'clown'))
        self.npcs.append(Character((width/2,height/2), self.camera_group, self, 'clown'))

        for i in range(20):
            random_x = randint(0,2000)
            random_y = randint(0,2000)
            Item((random_x, random_y), self.camera_group, self)

        
    def addItem(self, item, pos=(0, 0)):
        self.items.append(Item(item, pos, self))
        
    def draw(self):
        self.screen.fill(black)
        self.camera_group.update()
        self.camera_group.draw(self.screen)
        pygame.display.update()
       