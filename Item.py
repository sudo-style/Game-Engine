import pygame
from pygame.locals import *
import os
from GameObject import GameObject

class Item(pygame.sprite.Sprite, GameObject):
    def __init__(self, pos, group, parent, name, count= 1):
        super().__init__(group)
        self.image = pygame.image.load(os.path.join("sprites", 'items', name +".png")).convert_alpha()
        # todo have a default sound, and put the gun in its own class
        self.sound = pygame.mixer.Sound(os.path.join("sounds", "gun.WAV"))
        self.rect = self.image.get_rect(center = pos)
        self.parent = parent
        self.name = name
        self.pickUpTime = 0
        self.count = count
        self.pos = pos
    
    def drop(self):
        print(f"dropped {self.name}")
    
    def pickUp(self):
        print(f"picked up {self.name}")
        # add to inventory of the player
        self.parent.player.inventory.addItem(self.name, self.count)
        self.kill()

    def update(self):
        self.pickUpTime -= 1
        if self.parent.player.rect.colliderect(self.rect):       
            # if e is pressed then pick up
            if pygame.key.get_pressed()[K_p] and self.pickUpTime <= 0:
                self.pickUpTime = 20
                self.pickUp()

    def tryPickUp(self):
        if pygame.key.get_pressed()[K_p] and self.pickUpTime <= 0:
                self.pickUpTime = 20
                self.pickUp()
                
class Explosive(Item):
    def __init__(self, pos, group, parent, name = "bomb"):
        super().__init__(pos, group, parent, name)
        self.image = pygame.image.load(os.path.join("sprites", 'items', name +".png")).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.parent = parent
        
        self.damage = 100
        self.damageRadius = 100
        self.soundRadius = 500

        self.fuseTime = 200
        self.boolTriggered = False
        
        # sound
        self.sound = pygame.mixer.Sound(os.path.join("sounds", "grenade.wav"))
        self.fuse = pygame.mixer.Sound(os.path.join("sounds", "fuse.mp3"))
    
    def drop(self):
        print(f"dropped Explosive {self.name}")
        self.boolTriggered = True
        #self.fuse.play()

    def update(self):
        # trigger the explosive if the player is close enough
        self.pickUpTime -= 1
        if self.parent.player.rect.colliderect(self.rect):
            if pygame.mouse.get_pressed()[0] and self.pickUpTime <= 0:
                #self.fuse.play()
                self.boolTriggered = True
                self.pickUpTime = 20
            # if p is pressed then pick up
            self.tryPickUp()
                
        if (self.boolTriggered):
            self.fuseTime -= 1
            if (self.fuseTime <= 0):
                self.explode()
                
    
    def explode(self):
        self.sound.play()

        # draw the damage and sound radius
        pygame.draw.circle(self.parent.screen, (255,0,0), self.rect.center, self.damageRadius)
        pygame.draw.circle(self.parent.screen, (0,0,255), self.rect.center, self.soundRadius, 1)
        pygame.display.update()

        # check any characters in the sound radius
        for npc in self.parent.npcs:
            # check if the npc is in the radius of sound
            distance = self.getDistanceTo(npc)
            if (distance <= self.soundRadius):
                npc.setState('alert')
                npc.setSearchPos(self.rect.center, self.soundRadius)

            if (distance <= self.damageRadius):
                npc.health -= self.damage

        # explode explosives in the radius
        for explosive in self.parent.items:
            # check if the class is an explosive
            if not isinstance(explosive, Explosive): continue
            if explosive == self: break
            if (self.rect.colliderect(explosive.rect)):
                self.sound.play()
                explosive.explode()

        # remove the explosive from the map
        self.kill()
        
    def drop(self):
        self.boolTriggered = True
        self.fuse.play()

# player can posion food
# NPC can move, and eat food
class Food(Item):
    def __init__(self, pos, group, parent, name = "food"):
        super().__init__(pos, group, parent, name)
        self.image = pygame.image.load(os.path.join("sprites", 'items', name +".png")).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.parent = parent
        self.poisonStates = ['none', 'ko', 'lethal', 'emetic']
        self.poisonState = 'none'
    
    
    def gettingPoisoned(self, state):
        self.poisonState = self.poisonStates.index(state)
    
    def eat(self, target):
        # if the food was posioned then the target will be posioned
        if (self.poisonState != 'none'):
            target.poisoned(self.poisonState)
            print(f"{target.name} was poisoned")
        else: 
            print("MMM, that was good")
        self.kill()
