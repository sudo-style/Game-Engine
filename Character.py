import pygame 
from pygame.locals import *
import os
from Inventory import Inventory
from GameObject import GameObject
import math 
import copy
from random import randint

white = (255, 255, 255)
class Character(pygame.sprite.Sprite, GameObject):
    def __init__(self, pos, group, parent, name):
        super().__init__(group)
        self.name = name
        self.image = pygame.image.load(os.path.join('sprites', 'character', name, name + '.png')).convert_alpha()
        self.ko_image = pygame.image.load(os.path.join('sprites','character', name, 'ko.png')).convert_alpha()
        self.naked_image = pygame.image.load(os.path.join('sprites','character', name, 'naked.png')).convert_alpha()
        self.searchPos = pygame.Vector2()
        
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
        self.pos = pos
        self.searchPos = pygame.Vector2()

        self.states = ['idle', 'patrol', 'alert', 'search', 'combat', 'ko']
        self.statesIndex = 1
        
    def update(self):
        # lets the NPC breathe oxygen if not getting strangled and not KO yet
        self.breathing()
        if self.health <= 0: self.kill()
        self.pos = self.rect.center

    def breathing(self):
        self.oxygen += 1
        self.oxygen = min(self.oxygen, 100)

    def gettingSubdued(self):
        # oxygen decreases when getting strangled
        self.oxygen -= 2
        if self.oxygen <= 0: 
            self.ko()

    def getState(self):
        return self.states[self.statesIndex]

    def setState(self, state):
        if state in self.states:
            self.statesIndex = self.states.index(state)

    def setSearchPos(self, pos, radius):
        # random position within the radius
        radius = radius / 4 # closer but with small variation
        self.searchPos = pygame.Vector2(pos[0] + randint(-radius, radius), pos[1] + randint(-radius, radius))

    def nextWaypoint(self):
        self.waypointIndex += 1

    def movementController(self): # priority queue
        state = self.getState()
        
        # if knocked out, then can't do anything else
        if state == 'ko': return 
        
        # if alerted, then go to the alert position
        if state == 'alert': 
            self.alert()
            return
        
        # if in combat, then shoot at the player
        if state == 'combat':
            self.combat()
            print("COMBAT")
            return

        # if no special conditions are met, then this is the default state of the path of the NPC
        waypointState = self.waypoints[self.waypointIndex][0]
        if waypointState == 'patrol': self.patrol()  # move towards the next waypoint
        if waypointState == 'search': self.search() # rotate to the direction 
        if waypointState == 'idle': self.idle()  # pause for self.waypoints[self.waypointIndex][1] frames
        if waypointState == 'dir': self.rotate() # rotate to the direction 
        
        # goes to the begining of the path
        if self.waypointIndex >= len(self.waypoints):
            self.waypointIndex = 0
            self.waypoints = copy.deepcopy(self.originalWaypoints)  # Restore original waypoints using deep copy

    def rotate(self):
        angle = self.waypoints[self.waypointIndex][1]
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.nextWaypoint()
    
    def ko(self):
        self.image = self.ko_image
        self.KO = True
        self.setState('ko')

    def alert(self):
        # be idle for a couple seconds, then go to the position of the alert sound

        # make a new waypoint for the NPC
        print("allerted")
        self.waypoints = [['idle', 200], ['patrol', self.searchPos], ['search', 200], ['dir', 45], ['search', 100], ['dir', 135], ['search', 200]]
        self.waypointIndex = 0
        self.setState('patrol')

    def search(self):        
        # decreases the search time
        self.waypoints[self.waypointIndex][1] -= 1
        # if the NPC is close to the player then go into combat mode
        player = self.parent.player
        angleNPCtoPlayer = self.getDirectionTo(player)
        if self.isInLineOfSight(player, angleNPCtoPlayer, 10):
            print("Lets throw hands")
            self.setState('combat')
        if self.waypoints[self.waypointIndex][1] <= 0: self.nextWaypoint()
        
    def patrol(self):
        self.posWayPoint = self.waypoints[self.waypointIndex][1]
        self.direction = pygame.math.Vector2(self.posWayPoint[0] - self.rect.centerx, self.posWayPoint[1] - self.rect.centery)
        if self.direction.length() > 0:
            self.direction.normalize_ip()
        self.rect.center += self.direction * self.speed
        # rotate the image to face the direction of the movement
        self.angle = (180 / math.pi) * math.atan2(self.direction.y, self.direction.x)
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)
        # if the NPC is close the the search position, then go to the next waypoint
        if self.rect.collidepoint(self.searchPos): self.nextWaypoint()
    
    def idle(self):
        self.waypoints[self.waypointIndex][1] -= 1
        # if the NPC is done being idle, then go to the next waypoint
        if self.waypoints[self.waypointIndex][1] <= 0: self.nextWaypoint()


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
        self.pos = self.rect.center
    
    def shoot(self):
        # todo find a better way to get the current weapon, maybe use a dictionary with string keys and values as the items themselves
        currentWeapon = self.parent.items[-1]
        currentWeapon.sound.play()
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
                    npc.ko()
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
            if closest_npc != None: closest_npc.ko()
            pygame.draw.line(self.parent.screen, white, player_pos, line_endpoint, 2)
        
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
        currentWeapon = self.inventory.currentWeapon()

        # subdue if NPC is close enough
        if currentWeapon == 'fiberWire':
            # check if npc is close to players
            for npc in self.parent.npcs:                
                if self.rect.colliderect(npc.rect):
                    # subdue the npc
                    self.subdue(npc)
        
        if currentWeapon == 'gun':
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
        
        self.waypoints = [['patrol', (0, 0)], ['idle', 200], ['patrol', (100, 100)], ['patrol', (200, 200)], ['patrol', (self.parent.width, self.parent.height)], ['idle', 100]]
        self.originalWaypoints = copy.deepcopy(self.waypoints)  # Deep copy of original waypoints
        self.waypointIndex = 0

    def update(self):
        self.movementController() # controls movements of the NPC
        self.breathing()
        if self.health <= 0: self.kill()
        self.pos = self.rect.center

    def combat(self):
        # shoot at the player
        pass