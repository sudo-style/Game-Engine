import pygame 
from pygame.locals import *
import os
from Inventory import Inventory
from GameObject import GameObject
#from Blood import Blood
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
        self.blood_texture = pygame.image.load(os.path.join('sprites','character', 'blood', 'blood0.png')).convert_alpha()
        
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
        self.maxHealth = 100

        self.suitName = name
        self.pos = pos

    def updateHealth(self):
        blood_textures = {
            range(0, 25): 'blood3.png',
            range(26, 51): 'blood2.png',
            range(51, 76): 'blood1.png',
            range(76, 100): 'blood0.png'
        }

        for health_range, blood_texture_name in blood_textures.items():
            if self.health in health_range:
                self.blood_texture = pygame.image.load(os.path.join('sprites', 'character', 'blood', blood_texture_name)).convert_alpha()
                break


class Player(Character):
    def __init__(self, pos, group, parent, name = "player"):
        super().__init__(pos, group, parent, name)
        self.inventory = Inventory(self.parent)
        self.inputDelay = 0
        self.speed = 5

    def update(self):
        self.input()
        self.updateHealth()
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

class NPC(Character):
    def __init__(self, pos, group, parent, name = "clown"):
        super().__init__(pos, group, parent, name)

        self.states = ['idle', 'patrol', 'alert', 'search', 'combat', 'ko']
        self.statesIndex = 1
        self.searchPos = pygame.Vector2()
        self.waypoints = [['patrol', (0, 0)], 
                          ['patrol', (100, 100)], 
                          ['patrol', (200, 200)], 
                          ['idle', 200],
                          ['patrol', [parent.width/2, parent.height/2]]]
        self.originalWaypoints = copy.deepcopy(self.waypoints)  # Deep copy of original waypoints
        self.oxygen = 100
        self.KO = False
        
    def breathing(self):
        self.oxygen = min(self.oxygen + 1, 100)

    def gettingSubdued(self):
        # oxygen decreases when getting strangled
        self.oxygen -= 2
        if self.oxygen <= 0: self.ko()

    def update(self):
        self.movementController() # controls movements of the NPC
        self.breathing()
        self.updateHealth()
        if self.health <= 0: self.kill()
        self.pos = self.rect.center

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
        print(self.waypoints)
        if self.lenWaypoints() > 0: self.waypoints.pop()
        else: self.waypoints = copy.deepcopy(self.originalWaypoints)

    def getWaypoint(self):
        return self.waypoints[-1]
    
    def lenWaypoints(self):
        return len(self.waypoints)
    
    def currentWaypoint(self): # returns the current waypoint
        return self.waypoints[self.lenWaypoints()-1]
    
    def movementController(self): # priority queue
        state = self.getState()
        
        # if knocked out, then can't do anything else
        if self.KO: return
        
        # if alerted, then go to the alert position
        if state == 'alert': 
            self.alert()
            print("ALERT")
            return
        
        if state == 'eat':
            #self.eat()
            print("EAT")
            return

        # if no special conditions are met, then this is the default state of the path of the NPC
        waypointState, waypointValue = self.getWaypoint()
        
        waypointState = self.getWaypoint()[0]
        #print("waypointState: " + waypointState)
        if waypointState == 'patrol': self.patrol()  # move towards the next waypoint
        if waypointState == 'search': self.search() # rotate to the direction 
        if waypointState == 'idle': self.idle()  # pause for self.waypoints[self.waypointIndex][1] frames
        if waypointState == 'dir': self.rotate() # rotate to the direction 
        
        # goes to the begining of the path
        if self.lenWaypoints() == 0: self.waypoints = copy.deepcopy(self.originalWaypoints)  # Restore original waypoints using deep copy

    def rotate(self):
        angle = self.waypoints[-1][1]
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.nextWaypoint()
    
    def ko(self):
        self.image = self.ko_image
        self.KO = True
        self.setState('ko')

    def eat(self):
        # find the closest food
        closestFood = None
        closestDistance = 30
        for food in self.parent.foods:
            distance = self.getDistanceTo(food)
            if distance < closestDistance:
                closestDistance = distance
                closestFood = food
        
        # eat the food
        if closestFood != None: closestFood.eat(self)

    def alert(self):
        # be idle for a couple seconds, then go to the position of the alert sound

        # make a new waypoint for the NPC
        print("allerted")
        self.waypoints = [['search', 200], ['dir', 45], ['search', 200], ['dir', 135], ['search', 200], ['patrol' , self.searchPos], ['idle', 200]]
        self.setState('patrol')

    def search(self):        
        # decreases the search time
        self.waypoints[-1][1] -= 1
        # if the NPC is close to the player then go into combat mode
        player = self.parent.player
        angleNPCtoPlayer = self.getDirectionTo(player)
        if self.isInLineOfSight(player, angleNPCtoPlayer, 10):
            print("Lets throw hands")
            self.setState('combat')
        if self.waypoints[-1][1] <= 0: self.nextWaypoint()
        
    def patrol(self):
        waypointState, waypointValue = self.getWaypoint()
        
        pos = GameObject(waypointValue)
        if self.getDistanceTo(pos) < self.speed: 
            print("NEXT WAYPOINT")
            self.nextWaypoint()
            return

        self.direction = pygame.math.Vector2(waypointValue[0] - self.rect.centerx, waypointValue[1] - self.rect.centery)
        if self.direction.length() > 0:
            self.direction.normalize_ip()
        self.rect.center += self.direction * self.speed
        # rotate the image to face the direction of the movement
        self.angle = (180 / math.pi) * math.atan2(self.direction.y, self.direction.x)
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)
        # if the NPC is close the the search position, then go to the next waypoint

    def idle(self):
        self.waypoints[self.lenWaypoints()-1][1] -= 1
        # if the NPC is done being idle, then go to the next waypoint
        if self.waypoints[self.lenWaypoints()-1][1] <= 0: self.nextWaypoint()

class Guard(NPC):
    def __init__(self, pos, group, parent, name = "guard"):
        super().__init__(pos, group, parent, name)

        self.waypoints = [['patrol', (0, 0)], 
                          ['patrol', (100, 100)], 
                          ['patrol', (200, 200)], 
                          ['idle', 200],
                          ['patrol', (30,30)]]
        self.originalWaypoints = copy.deepcopy(self.waypoints)  # Deep copy of original waypoints

    def combat(self):
        # try to follow the player and shoot at them
        player = self.parent.player
        angleNPCtoPlayer = self.getDirectionTo(player)
        if self.isInLineOfSight(player, angleNPCtoPlayer, 10):
            self.shoot()
        else:
            self.setState('alert')
            self.setSearchPos(player.rect.center, 100)
            self.alert()
        
        # if the player is close enough, then go into combat mode
        if self.getDistanceTo(player) < 100:
            print("Lets throw hands")
            self.setState('combat')
        else:
            self.setState('alert')
            self.setSearchPos(player.rect.center, 100)
            self.alert()

    def shoot(self):
        pass

    def movementController(self): # priority queue
        state = self.getState()
        
        # if knocked out, then can't do anything else
        if self.KO: return
        
        # if alerted, then go to the alert position
        if state == 'alert': 
            self.alert()
            print("ALERT")
            return

        if state == 'combat':
            self.combat()
            print("COMBAT")
            return

        # if no special conditions are met, then this is the default state of the path of the NPC
        waypointState, waypointValue = self.getWaypoint()
        
        waypointState = self.getWaypoint()[0]
        #print("waypointState: " + waypointState)
        if waypointState == 'patrol': self.patrol()  # move towards the next waypoint
        if waypointState == 'search': self.search() # rotate to the direction 
        if waypointState == 'idle': self.idle()  # pause for self.waypoints[self.waypointIndex][1] frames
        if waypointState == 'dir': self.rotate() # rotate to the direction 
        
        # goes to the begining of the path
        if self.lenWaypoints() == 0: self.waypoints = copy.deepcopy(self.originalWaypoints)  # Restore original waypoints using deep copy