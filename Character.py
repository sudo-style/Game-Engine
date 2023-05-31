import pygame
from pygame.locals import *
import os
from Inventory import Inventory
import math
import copy

white = (255, 255, 255)
class Character(pygame.sprite.Sprite):
    def __init__(self, pos, group, parent, name):
        super().__init__(group)
        self.name = name
        self.image = pygame.image.load(os.path.join('sprites', 'character', name, name + '.png')).convert_alpha()
        self.ko_image = pygame.image.load(os.path.join('sprites','character', name, 'ko.png')).convert_alpha()
        self.naked_image = pygame.image.load(os.path.join('sprites','character', name, 'naked.png')).convert_alpha()
        
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 3
        self.angle = 0
        oldCenter = self.rect.center
        self.oldCenter = oldCenter
        self.group = group
        self.parent = parent
        self.health = 100
        self.oxygen = 100
        self.KO = False
        self.suitName = name
        
    def update(self):
        # if an NPC and a player collide then print "hello"
        if self.parent.player.rect.colliderect(self.rect):
            # if player clicks on the NPC then print "hello"
            if pygame.mouse.get_pressed()[0]:
                print("hello")

        # lets the NPC breathe oxygen if not getting strangled and not KO yet
        self.breathing()
        if self.health <= 0: self.kill()

    def ko(self):
        self.image = self.ko_image
        self.KO = True


    def gettingSubdued(self):
        # oxygen decreases when getting strangled
        self.oxygen -= 2
        if self.oxygen <= 0: 
            self.ko()
    
    def breathing(self):
        self.oxygen += 1
        if self.oxygen > 100: self.oxygen = 100

class Player(Character):
    def __init__(self, pos, group, parent, name = "player"):
        super().__init__(pos, group, parent, name)
        self.inventory = Inventory(self.parent)
        self.inputDelay = 0
        self.speed = 5

    def update(self):
        self.input()
        self.draw()
        self.rect.center += self.direction * self.speed
        self.inventory.update()
        pygame.display.update()
        self.inputDelay -= 1
    
    def shoot():
        print('shoot')

    def input(self):
        self.movement()
        self.mouseRotation()
        
        # if m is pressed,
        keysPressed = pygame.key.get_pressed()
 
        if keysPressed[K_b]:
            self.weaponAttack()
 
        if keysPressed[K_t] and self.inputDelay < 0:
            self.inputDelay = 30
            self.takeDisguise()
            
    def takeDisguise(self):
        # check if player is close to the suit
        for npc in self.parent.npcs:
            if self.rect.colliderect(npc.rect):
                # if player clicks on suit then print "suit up"
                if npc.KO:
                    # take the disguise
                    newSuit = npc.suitName
                    self.original_image = pygame.image.load(os.path.join('sprites', 'character', newSuit, newSuit + '.png')).convert_alpha()
                    npc.suitName = self.suitName
                    self.suitName = newSuit
                    npc.image = npc.naked_image
                    self.rect = self.image.get_rect(center = self.rect.center)
                    
    def weaponAttack(self):
        # subdue if NPC is close enough
        if self.inventory.currentWeapon() == 'fiberWire':
            # check if npc is close to players
            for npc in self.parent.npcs:                
                if self.rect.colliderect(npc.rect):
                    # subdue the npc
                    self.subdue(npc)
        
        if self.inventory.currentWeapon() == 'gun':
            self.shoot()
            pass

    def subdue(self, npc):
        # drag the npc to the player
        npc.gettingSubdued()
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

class NPC(Character):
    def __init__(self, pos, group, parent, name="guard"):
        super().__init__(pos, group, parent, name)
        self.states = ['idle', 'patrol', 'alert', 'search', 'combat', 'ko']
        self.statesIndex = 1
        self.waypoints = [['patrol', (0, 0)], ['idle', 200], ['patrol', (100, 100)], ['patrol', (200, 200)], ['patrol', (self.parent.width, self.parent.height)], ['idle', 100]]
        self.originalWaypoints = copy.deepcopy(self.waypoints)  # Deep copy of original waypoints
        self.waypointIndex = 0
        self.searchPos = pygame.Vector2()

    def update(self):
        self.waypointsControler() # controls movements of the NPC
        self.breathing()
        if self.health <= 0: self.kill()

    def waypointsControler(self):
        state = self.getState()
        
        if state == 'ko': 
            return 
        if state == 'search':
            self.search()  # move towards the position of the sound
            return
        if state == 'combat':
            self.combat()
        state = self.waypoints[self.waypointIndex][0]
        if state == 'patrol': self.patrol()  # move towards the next waypoint
        if state == 'idle': self.idle()  # pause for self.waypoints[self.waypointIndex][1] frames

        if self.waypointIndex >= len(self.waypoints):
            self.waypointIndex = 0
            self.waypoints = copy.deepcopy(self.originalWaypoints)  # Restore original waypoints using deep copy

    def combat(self):
        # shoot at the player
        pass

    def getState(self):
        return self.states[self.statesIndex]

    def search(self):
        self.direction = pygame.math.Vector2(self.searchPos[0] - self.rect.centerx, self.searchPos[1] - self.rect.centery)
        if self.direction.length() > 0:
            self.direction.normalize_ip()
        self.rect.center += self.direction * self.speed

        # if the NPC is close to the player then go into combat mode
        if self.rect.colliderect(self.parent.player.rect):
            self.statesIndex = 4


    def idle(self):
        self.waypoints[self.waypointIndex][1] -= 1
        if self.waypoints[self.waypointIndex][1] <= 0:
            self.waypointIndex += 1

    def patrol(self):
        self.direction = pygame.math.Vector2(self.waypoints[self.waypointIndex][1][0] - self.rect.centerx, self.waypoints[self.waypointIndex][1][1] - self.rect.centery)
        if self.direction.length() > 0:
            self.direction.normalize_ip()
        self.rect.center += self.direction * self.speed

        if self.rect.collidepoint(self.waypoints[self.waypointIndex][1]):
            self.waypointIndex += 1

    def ko(self):
        self.image = self.ko_image
        self.KO = True
        self.statesIndex = 5
