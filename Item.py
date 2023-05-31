import pygame
from pygame.locals import *
import os

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, group, parent, name= "camera"):
        super().__init__(group)
        self.image = pygame.image.load(os.path.join("sprites", name +".png")).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.parent = parent

class Explosive(Item):
    def __init__(self, pos, group, parent, name = "bomb"):
        super().__init__(pos, group, parent, name)
        self.image = pygame.image.load(os.path.join("sprites", name +".png")).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.parent = parent
        
        self.damage = 100
        self.radius = 100
        self.fuseTime = 40
        self.boolTriggered = False


    def update(self):
        if (self.boolTriggered):
            self.fuseTime -= 1
            if (self.fuseTime <= 0):
                self.explode()
    
    def explode(self):
        # TODO: add explosion animation
        # TODO: add explosion sound
        
        # check any characters in the radius
        for character in self.parent.npcs:
            if (self.rect.colliderect(character.rect)):
                character.health -= self.damage
        
        # remove the explosive from the map
        self.kill()
        
    def dropped(self):
        self.boolTriggered = True

        