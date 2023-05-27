import pygame
from pygame.locals import *
import os

class Item:
    def __init__(self, name, pos, parent):
        self.pos = pos
        self.name = name
        self.original_sprite = pygame.image.load(os.path.join("sprites", name + ".png"))
        self.sprite = self.original_sprite.copy()
        self.rect = self.sprite.get_rect(center=self.pos)
        self.parent = parent

    def draw(self):
        self.parent.screen.blit(self.sprite, self.pos, self.parent.camera)

    def update(self):
        self.draw()

        # if the player collides TODO somthing is wrong here 
        if self.rect.colliderect(self.parent.player.rect):
            self.parent.player.inventory.addItem(self.name)
            self.parent.items.remove(self)
            del self