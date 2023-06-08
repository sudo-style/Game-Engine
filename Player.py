import pygame 
from pygame.locals import *
import os

from GameObject import GameObject
from Character import Character
from Inventory import Inventory

#from Blood import Blood
import math 
import copy
from random import randint

white = (255, 255, 255)


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
        self.inputDelay = max(self.inputDelay - 1, 0)
        self.pos = self.rect.center
    
    def shoot(self):
        # todo find a better way to get the current weapon, maybe use a dictionary with string keys and values as the items themselves
        currentWeapon = self.inventory.currentWeapon()
        #currentWeapon.sound.play()
        # Get the player's position
        player_pos = self.rect.center
        mouse_pos = pygame.mouse.get_pos()

        # Calculate the ray direction
        delta_x = mouse_pos[0] - player_pos[0] + self.group.offset.x
        delta_y = mouse_pos[1] - player_pos[1] + self.group.offset.y
        playerToMouseAngle = math.atan2(delta_y, delta_x)

        # Calculate a long line endpoint based on the ray direction
        line_length = 1000  # Adjust the line length as needed
        line_endpoint_x = player_pos[0] + line_length * math.cos(playerToMouseAngle)
        line_endpoint_y = player_pos[1] + line_length * math.sin(playerToMouseAngle)
        line_endpoint = (line_endpoint_x, line_endpoint_y)

        # Initialize the closest NPC and its distance
        closest_npc = None
        closest_distance = float('inf')

        # will shoot all of the NPCs in the line of sight
        if self.inventory.currentWeapon() == 'sniper':
            furthestDistance = 0
            # Check the raycast against each NPC object
            for npc in self.parent.npcs:
                npc_pos = npc.rect.center
                distance = self.getDistanceTo(npc)
                # Calculate the angle between the NPC and the player
                if self.isInLineOfSight(npc, playerToMouseAngle, 10):
                    if distance > furthestDistance: 
                        furthestDistance = distance
                        line_endpoint = npc_pos
                    npc.health -= 25
                    npc.updateHealth()
            pygame.draw.line(self.parent.screen, white, player_pos, line_endpoint, 2)
            return
        
        else: # shoots the closest NPC in the line of sight
            for npc in self.parent.npcs:
                npc_pos = npc.rect.center
                distance = self.getDistanceTo(npc)
                # Check if the NPC is closer than the previous closest NPC
                if distance < closest_distance:
                    if self.isInLineOfSight(npc, playerToMouseAngle, 10):
                        closest_distance = distance
                        line_endpoint = npc_pos
                        closest_npc = npc            
            if closest_npc != None: 
                closest_npc.health -= 25
                closest_npc.updateHealth()
                #closest_npc.ko()
            pygame.draw.line(self.parent.screen, white, player_pos, line_endpoint, 2)
        
    def input(self):
        self.movement()
        self.mouseRotation()
        
        # if m is pressed,
        keysPressed = pygame.key.get_pressed()
 
        if keysPressed[K_b]:
            self.weaponAttack()
 
        if keysPressed[K_t] and self.inputDelay <= 0:
            self.inputDelay = 30 # don't want them to accidentally spam it
            self.takeDisguise()
            
    def takeDisguise(self):
        # check if player is close to the suit
        print("t pressed")
        for npc in self.parent.npcs:
            if self.rect.colliderect(npc.rect):
                # if player clicks on suit then print "suit up"
                if npc.KO:
                    # take the disguise
                    tempSuit = self.suitName
                    self.suitName = npc.suitName
                    npc.suitName = tempSuit
                    self.original_image = pygame.image.load(os.path.join('sprites', 'character', self.suitName, self.suitName + '.png')).convert_alpha()
                    npc.original_image = pygame.image.load(os.path.join('sprites', 'character', npc.suitName, npc.suitName + '.png')).convert_alpha()
                    
    def weaponAttack(self):
        currentWeapon = self.inventory.currentWeapon()

        # subdue if NPC is close enough
        if currentWeapon == 'fiberWire':
            # check if npc is close to players
            for npc in self.parent.npcs:                
                if self.rect.colliderect(npc.rect):
                    # subdue the npc
                    self.subdue(npc)
                    return
        
        if currentWeapon == 'gun' and self.inputDelay < 0:
            # if the player has bullets in the gun
            if self.inventory.currentWeaponsCount() > 0:
                self.shoot()

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
        # Create a new surface for the transformed image
        transformed_image = pygame.Surface(self.original_image.get_size(), pygame.SRCALPHA)

        # Add the blood splatter to the original image
        transformed_image.blit(self.original_image, (0, 0))
        transformed_image.blit(self.blood_texture, (0, 0))

        # Rotate the transformed image
        rotated_image = pygame.transform.rotate(transformed_image, -self.angle)
        self.image = rotated_image

        # Update the rectangle based on the transformed image
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.inventory.visible: self.inventory.drawCarousel()