import pygame
from pygame.locals import *
import os
from Inventory import Inventory
import math

white = (255, 255, 255)
class Character:
    def __init__(self, x, y, sprite, parent):
        self.pos = (x, y)
        # self.direction = 0
        self.original_sprite = pygame.image.load(os.path.join("sprites", sprite + ".png"))
        self.sprite = self.original_sprite.copy()
        self.rect = self.sprite.get_rect(center=self.pos)
        self.parent = parent

    def draw(self):
        pass

    def spawn(self):
        pass

class Player(Character):
    def __init__(self, x, y, parent):
        super().__init__(x, y, "player", parent)
        self.shootDelay = 0
        self.inventory = Inventory(parent)

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)

    def rotate(self, angle):
        self.sprite = pygame.transform.rotate(self.original_sprite, -angle)
        self.rect = self.sprite.get_rect(center=self.rect.center)

    def update(self):
        # Update the inventory
        self.inventory.update()

        # Movement
        speed = 3
        keysPressed = pygame.key.get_pressed()
        dx, dy = 0, 0
        self.shootDelay -= 1

        # Input for movement
        if keysPressed[K_w]: dy -= 1
        if keysPressed[K_s]: dy += 1
        if keysPressed[K_a]: dx -= 1
        if keysPressed[K_d]: dx += 1

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            magnitude = math.sqrt(dx ** 2 + dy ** 2)
            dx /= magnitude
            dy /= magnitude
        dx *= speed
        dy *= speed
        self.move(dx, dy)

        # Rotation
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.degrees(math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx))
        self.rotate(angle)

        # Shooting
        # TODO: make this have a cooldown period instead of once per frame so you can't just hold down the mouse button
        if (pygame.mouse.get_pressed()[0] and self.shootDelay <= 0):
            # Make a line from player to mouse
            pygame.draw.line(self.parent.screen, white, self.rect.center, (mouse_x, mouse_y), 2)
            pygame.display.flip()
            self.shootDelay = 20
    def draw(self):
        self.parent.screen.blit(self.sprite, self.rect.topleft)
        
        if self.inventory.visible:
            self.inventory.draw()

    

class NPC(Character):
    def __init__(self, x, y, sprite='clown'):
        super().__init__(x, y, sprite)
        self.states = ['path', 'investigate', 'sus', 'panic', 'dead']
        self.state = self.states[0]
        self.path = [(0, 0), (100, 0), (100, 100), (0, 100)]  # Keeps looping through path to test

    def rotate(self, angle):
        self.sprite = pygame.transform.rotate(self.original_sprite, -angle)
        self.rect = self.sprite.get_rect(center=self.rect.center)