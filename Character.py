import pygame
from pygame.locals import *
import os
from Inventory import Inventory
import math

white = (255, 255, 255)
class Character(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.image = pygame.image.load('sprites/player.png').convert_alpha()
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.angle = 0
        oldCenter = self.rect.center
        self.oldCenter = oldCenter
        self.group = group

class Player(Character):
    def __init__(self, pos, group):
        super().__init__(pos, group)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]: self.direction.y = -1
        elif keys[pygame.K_DOWN]: self.direction.y = 1
        else: self.direction.y = 0

        if keys[pygame.K_RIGHT]: self.direction.x = 1
        elif keys[pygame.K_LEFT]: self.direction.x = -1
        else: self.direction.x = 0

        # get the angle of the mouse and the center of the screen
        mouse_pos = pygame.mouse.get_pos()
        delta_x = mouse_pos[0] - self.rect.centerx + self.group.offset.x
        delta_y = mouse_pos[1] - self.rect.centery + self.group.offset.y
        self.angle = (180 / math.pi) * math.atan2(delta_y,delta_x)

        # rotate the image
        oldCenter = self.rect.center
        self.oldCenter = oldCenter
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter

    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed
        print(self.rect.center)