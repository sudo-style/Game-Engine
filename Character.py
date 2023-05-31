import pygame
from pygame.locals import *
import os
from Inventory import Inventory
import math

white = (255, 255, 255)
class Character(pygame.sprite.Sprite):
    def __init__(self, pos, group, parent, name = "clown"):
        super().__init__(group)
        self.name = name
        self.image = pygame.image.load(os.path.join('sprites', 'character', name, name + '.png')).convert_alpha()
        self.ko_image = pygame.image.load(os.path.join('sprites','character', name, 'ko.png')).convert_alpha()
        self.naked_image = pygame.image.load(os.path.join('sprites','character', name, 'naked.png')).convert_alpha()
        
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
        self.oxygen = 100
        self.KO = False

    def update(self):
        # if an NPC and a player collide then print "hello"
        if self.parent.player.rect.colliderect(self.rect):
            # if player clicks on the NPC then print "hello"
            if pygame.mouse.get_pressed()[0]:
                print("hello")

        # lets the NPC breathe oxygen if not getting strangled and not KO yet
        self.oxygen += 1
        if self.oxygen > 100: self.oxygen = 100
            
        if self.health <= 0: self.kill()

    def ko(self):
        self.image = self.ko_image
        self.KO = True

    def gettingStrangled(self):
        # oxygen decreases when getting strangled
        self.oxygen -= 2
        if self.oxygen <= 0: 
            self.ko()

class Player(Character):
    def __init__(self, pos, group, parent, name = "player"):
        super().__init__(pos, group, parent, name)
        self.image = pygame.image.load(os.path.join('sprites', 'character', name, name + '.png')).convert_alpha()
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center = pos)
        self.inventory = Inventory(self.parent)
        self.inventoryPause = 0

    def update(self):
        self.input()
        self.draw()
        self.rect.center += self.direction * self.speed
        self.inventory.update()

    def input(self):
        self.movement()
        self.mouseRotation()
        
        # if m is pressed,
        keysPressed = pygame.key.get_pressed()
        if keysPressed[K_m]:
            self.weapon()
            print("pressed m")

        if keysPressed[K_t]:
            self.takeDisguise()
            

    def takeDisguise(self):
        # check if player is close to the suit
        for npc in self.parent.npcs:
            if self.rect.colliderect(npc.rect):
                # if player clicks on suit then print "suit up"
                if npc.KO:
                    # take the disguise
                    self.image = pygame.image.load(os.path.join('sprites', 'character', npc.name, npc.name + '.png')).convert_alpha()

                    self.original_image = self.image.copy()
                    npc.image = npc.naked_image
    
    def weapon(self):
        # strangle if NPC is close enough
        if self.inventory.currentWeapon() == 'fiberWire':
            # check if npc is close to players
            for npc in self.parent.npcs:                
                if self.rect.colliderect(npc.rect):
                    # if player clicks on npc then print "strangle"
                    self.strangle(npc)
                    print(npc.oxygen)
    
    def suitUp(self):
        # check if player is close to the suit
        for item in self.parent.items:
            if self.rect.colliderect(item.rect):
                # if player clicks on suit then print "suit up"
                self.inventory.addItem(item.name)
                item.kill()
                print("suit up")


    def strangle(self, npc):
        # drag the npc to the player
        npc.gettingStrangled()
        npc.rect.center = self.rect.center
        
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

    
    def draw(self):
        # rotate the image
        oldCenter = self.rect.center
        self.oldCenter = oldCenter
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter

        if self.inventory.visible: self.inventory.drawCarousel()
        pygame.display.update()
