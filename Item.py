import pygame
from pygame.locals import *
import os

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, group, parent, name= "fiberWire"):
        super().__init__(group)
        self.image = pygame.image.load(os.path.join("sprites", name +".png")).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.parent = parent
        self.name = name
    
    def drop(self):
        print(f"dropped {self.name}")

class Explosive(Item):
    def __init__(self, pos, group, parent, name = "bomb"):
        super().__init__(pos, group, parent, name)
        self.image = pygame.image.load(os.path.join("sprites", name +".png")).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.parent = parent
        
        self.damage = 100
        self.radius = 100
        self.fuseTime = 200
        self.boolTriggered = False

        # sound
        self.sound = pygame.mixer.Sound(os.path.join("sounds", "grenade.wav"))
        self.fuse = pygame.mixer.Sound(os.path.join("sounds", "fuse.mp3"))
    
    def drop(self):
        print(f"dropped Explosive {self.name}")
        self.boolTriggered = True
        self.fuse.play()


    def update(self):
        # trigger the explosive if the player is close enough
        if self.parent.player.rect.colliderect(self.rect):
            if pygame.mouse.get_pressed()[0]:
                self.boolTriggered = True

        if (self.boolTriggered):
            self.fuseTime -= 1
            if (self.fuseTime <= 0):
                self.explode()
                self.sound.play()
    
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
        self.fuse.play()

        