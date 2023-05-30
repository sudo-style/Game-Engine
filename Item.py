import pygame
from pygame.locals import *
import os

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, group, parent):
        super().__init__(group)
        self.image = pygame.image.load(os.path.join("sprites", "camera.png")).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.parent = parent