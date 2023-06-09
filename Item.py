import pygame
from pygame.locals import *
import os
from GameObject import GameObject

class Item(pygame.sprite.Sprite, GameObject):
    def __init__(self, pos, group, parent, name, count=1):
        super().__init__(group)
        self.image = pygame.image.load(os.path.join("sprites", 'items', name + ".png")).convert_alpha()
        # todo have a default sound, and put the gun in its own class
        self.sound = pygame.mixer.Sound(os.path.join("sounds", "gun.WAV"))
        self.rect = self.image.get_rect(center=pos)
        self.parent = parent
        self.name = name
        self.pickUpTime = 0
        self.count = count
        self.pos = pos

    def interact(self):
        pass

    def drop(self):
        #print(f"dropped {self.name}")
        pass

    def update(self):
        self.pickUpTime = max(self.pickUpTime - 1, 0)
        if self.parent.player.rect.colliderect(self.rect) and self.pickUpTime <= 0 and pygame.key.get_pressed()[K_f]:
            self.parent.player.inventory.addItem(self)
            self.kill()
                
class Explosive(Item):
    def __init__(self, pos, group, parent, name = "bomb"):
        super().__init__(pos, group, parent, name)
        self.image = pygame.image.load(os.path.join("sprites", 'items', name +".png")).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        
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
        self.pickUpTime = max(self.pickUpTime - 1, 0)
        #if self.parent.player.rect.colliderect(self.rect):
            #print(f"Colliding with player with {self.name}")
            #self.boolTriggered = True
            #self.tryToPickUp()
                
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
        self.poisonStates = ['none', 'ko', 'lethal', 'emetic']
        self.poisonState = 0

    def getPosionState(self):
        return self.poisonStates[self.poisonState]
    
    def gettingPoisoned(self, state):
        print('food is poisioned')
        self.poisonState = self.poisonStates.index(state)
    
    def eat(self, target):
        # if the food was posioned then the target will be posioned
        if (self.poisonStates[self.poisonState] == 'none'):
            print("MMM, that was good")
            self.kill()
            return
        print(f"{target.name} was poisoned")
        target.setState(self.poisonStates[self.poisonState])
        self.kill()

        if self.getPosionState()== 'ko':
            target.ko()


    def update(self):
        self.pickUpTime -= 1
        
        player = self.parent.player
        if self.parent.player.rect.colliderect(self.rect):
            if pygame.key.get_pressed()[K_e] and self.pickUpTime <= 0:
                self.pickUpTime = 20
                self.pickUp()
        
class Poison(Item):
    def __init__(self, pos, group, parent, name = "ko"):
        super().__init__(pos, group, parent, name)
        self.rect = self.image.get_rect(center = pos)
        self.posionType = ['injection', 'pill']
        self.poisonStates = ['none', 'ko', 'lethal', 'emetic']
        self.poisonState = 0
    
    def poison(self, target):
        print(f"{target.name} was poisoned")
        target.poisoned(self.poisonState)
        self.kill()

class Gun(Item):
    def __init__(self, pos, group, parent, name, count, fireRate):
        super().__init__(pos, group, parent, name, count)
        self.rect = self.image.get_rect(center = pos)
        self.fireRate = fireRate
        self.sound = pygame.mixer.Sound(os.path.join("sounds", "gun.WAV"))
    
    