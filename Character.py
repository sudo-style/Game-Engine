import pygame
from pygame.locals import *
import os
from Inventory import Inventory
import math

white = (255, 255, 255)
class Character:
    def __init__(self, pos, sprite, parent):
        self.pos = pos
        self.original_sprite = pygame.image.load(os.path.join("sprites", sprite + ".png"))
        self.sprite = self.original_sprite.copy()
        self.rect = self.sprite.get_rect(center= pos)
        self.parent = parent

    def draw(self):
        pass

    def spawn(self):
        pass

class Player(Character):
    def __init__(self, pos, parent):
        super().__init__(pos, "player", parent)
        self.shootDelay = 0
        self.inventory = Inventory(parent)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 3

    def rotate(self, angle):
        self.sprite = pygame.transform.rotate(self.original_sprite, -angle)
        self.rect = self.sprite.get_rect(center=self.rect.center)

    def movement(self):
        keysPressed = pygame.key.get_pressed()
        if keysPressed[K_w]: self.direction.y -= 1
        if keysPressed[K_s]: self.direction.y += 1
        if keysPressed[K_a]: self.direction.x -= 1
        if keysPressed[K_d]: self.direction.x += 1
        self.rect.center += self.direction * self.speed
        
        # normalize vector
        if self.direction.length() > 0:
            self.direction.normalize_ip()
            
    def rotation(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.degrees(math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx))
        self.rotate(angle)

    def shoot(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.shootDelay <= 0:
            # Make a line from player to mouse
            pygame.draw.line(self.parent.screen, white, self.rect.center, (mouse_x, mouse_y), 2)
            pygame.display.flip()
            self.shootDelay = 20
            print(f"player pos: {self.rect.center} item pos: {self.parent.items[0].pos}" )

    def update(self):
        self.movement()
        
        # Update the inventory
        self.inventory.update()
        self.shootDelay -= 1

        # Rotation
        self.rotation()
        self.shoot()
        self.direction = pygame.math.Vector2(0, 0)

    def draw(self):
        self.parent.screen.blit(self.sprite, self.rect.topleft)
        
        if self.inventory.visible:
            self.inventory.draw()

class NPC(Character):
    def __init__(self, pos, sprite='clown'):
        super().__init__(pos, sprite)
        self.states = ['path', 'investigate', 'sus', 'panic', 'dead']
        self.state = self.states[0]
        self.path = [(0, 0), (100, 0), (100, 100), (0, 100)]  # Keeps looping through path to test

    def rotate(self, angle):
        self.sprite = pygame.transform.rotate(self.original_sprite, -angle)
        self.rect = self.sprite.get_rect(center=self.rect.center)