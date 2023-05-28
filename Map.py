import pygame
from pygame.locals import *
import os
import math

from Item import Item
from Character import Player, NPC

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
playerKeys = [K_LEFT, K_RIGHT, K_UP, K_DOWN]

class Map:
    def __init__(self, name, width, height, screen, clock, fps):
        self.name = name
        self.descritpion = ""
        self.targets = []
        self.rooms = []
        self.items = []
        self.npcs = []
        self.original_sprite = pygame.image.load(os.path.join("sprites", "GroundFloor.png"))
        self.sprite = self.original_sprite.copy()
        self.player = Player((width/2, height/2), self)
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.camera = pygame.Rect(0, 0, self.width, self.height)
        
    def update(self):
        # Update the player
        self.player.update()
        for npc in self.npcs: npc.update()
        for item in self.items: item.update()

        self.clock.tick(self.fps)
        self.draw()

    def addItem(self, item, pos=(0, 0)):
        self.items.append(Item(item, pos, self))
        
    def draw(self):
        self.screen.fill(black)
        # Create a camera rect centered around the player
        # camera = pygame.Rect(0, 0, self.width, self.height)
        self.camera.center = self.player.rect.center

        # Draw the background image onto the screen relative to the camera position
        self.screen.blit(self.sprite, (0, 0), self.camera)

        # Draw player and other objects relative to the camera position
        self.player.draw()

        # Draw all items
        for item in self.items: item.draw()

        # Draw all NPCs
        for npc in self.npcs: npc.draw()

        

        pygame.display.flip()