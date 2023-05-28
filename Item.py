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
        self.parent.screen.blit(self.sprite, self.rect.topleft)

    def update(self):
        self.draw()
        # if the player collides TODO somthing is wrong here 
        keysPressed = pygame.key.get_pressed()
        if self.rect.colliderect(self.parent.player.rect) and keysPressed[K_e]:
            self.parent.player.inventory.addItem(self.name)
            self.parent.items.remove(self)
            del self