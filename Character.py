import pygame
from pygame.locals import *
import os
from Inventory import Inventory
import math

white = (255, 255, 255)
class Character(pygame.sprite.Sprite):
    def __init__(self, pos, group, parent, name = "clown"):
        super().__init__(group)
        self.image = pygame.image.load(os.path.join('sprites',name + '.png')).convert_alpha()
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.angle = 0
        oldCenter = self.rect.center
        self.oldCenter = oldCenter
        self.group = group
        self.parent = parent
        self.health = 100
        self.name = name
        
    def update(self):
        # if an NPC and a player collide then print "hello"
        if self.parent.player.rect.colliderect(self.rect):
            # if player clicks on the NPC then print "hello"
            if pygame.mouse.get_pressed()[0]:
                print("hello")


class Player(Character):
    def __init__(self, pos, group, parent, name = "player"):
        super().__init__(pos, group, parent, name)
        self.image = pygame.image.load(os.path.join('sprites',name + '.png')).convert_alpha()
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center = pos)
        self.inventory = Inventory(self.parent)
        self.inventoryPause = 0

    def update(self):
        self.input()
        self.draw()
        self.rect.center += self.direction * self.speed
        self.inventory.update()
    
    def draw(self):
        # rotate the image
        oldCenter = self.rect.center
        self.oldCenter = oldCenter
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter

        if self.inventory.visible:
            self.inventory.draw()
        
        pygame.display.update()

    def input(self):
        self.movement()
        self.mouseRotation()
        
    def movement(self):
        keysPressed = pygame.key.get_pressed()
        if keysPressed[K_w]: self.direction.y -= 1
        if keysPressed[K_s]: self.direction.y += 1
        if keysPressed[K_a]: self.direction.x -= 1
        if keysPressed[K_d]: self.direction.x += 1

        # normalize vector
        if self.direction.length() > 0:
            self.direction.normalize_ip()
        self.rect.center += self.direction * self.speed

        self.direction = pygame.math.Vector2(0, 0)

    def mouseRotation(self):
        # get the angle of the mouse and the center of the screen
        mouse_pos = pygame.mouse.get_pos()
        delta_x = mouse_pos[0] - self.rect.centerx + self.group.offset.x
        delta_y = mouse_pos[1] - self.rect.centery + self.group.offset.y
        self.angle = (180 / math.pi) * math.atan2(delta_y,delta_x)
