import pygame
from pygame.locals import *
import os
import math

explosives = ['bomb', 'tnt', 'grenade', 'rubber duck']
guns = ['smg', 'pistol', 'siniper']
keep = ['fiberWire']

class Inventory:
    def __init__(self, grandparent):
        self.grandparent = grandparent
        self.maxInventory = {'smg': 100, 'pistol': 69, 'siniper':100}        
        self.inventory = {}
        self.updated = []
        self.addItem('fiberWire')
        self.addItem('tnt')
        #self.addItem('gun',30)
        self.visible = True
        self.interactDelay = 0

    def addItem(self, item, count = 1):
        print("adding item " + item)
        if item not in self.inventory:
            self.inventory[item] = count
            self.updated = [item] + self.updated
            return
        self.updated.remove(item)
        self.updated = [item] + self.updated
        self.inventory[item] += count
        if item in self.maxInventory:
            self.inventory[item] = min(self.inventory[item],self.maxInventory[item])

    def removeItem(self):
        if len(self.updated) <= 0: return
    
        item = self.updated[0]
        print("removing: " + item)
        
        isGun = item in self.maxInventory
        willRemoveAll = self.inventory[item] <= 1
        if isGun or willRemoveAll:
            self.inventory.pop(item)
            self.updated.remove(item)
            return
        self.inventory[item]-=1 

    def shoot(self):
        gun = self.updated[0]
        print("trying to shoot " + gun)
        if not gun in self.maxInventory:
            print("not a gun")
            return
        print("was a gun")
        if self.inventory[gun] > 0:        
            self.inventory[gun] -= 1

    def print(self):
        print(f"inventory: {self.inventory}")
        print(f"updated: {self.updated}\n")

    def selectLeft(self):
        self.updated = [self.updated[-1]] + self.updated[0:-1]
        
    def selectRight(self):
        self.updated = self.updated[1:] + self.updated[:1]
    
    def update(self):
        # a short delay between interactions
        self.interactDelay -= 1
        
        # if v is pressed, toggle visibility
        keysPressed = pygame.key.get_pressed()
        if keysPressed[K_v] and self.interactDelay <= 0:
            self.visible = not self.visible
            self.interactDelay = 30

        # everything below needs the inventory to be visible
        if not self.visible: return
        
        # rotate the carousel for directional keys
        if keysPressed[K_LEFT] and self.interactDelay <= 0:
            self.selectLeft()
            self.interactDelay = 20

        if keysPressed[K_RIGHT] and self.interactDelay <= 0:
            self.selectRight()
            self.interactDelay = 20            

        # if e is pressed drop item:
        if keysPressed[K_e] and self.updated[0] not in keep and self.interactDelay <= 0:
            
            if self.updated[0] in guns: self.shoot()
            
            elif self.updated[0] in explosives: 
                self.grandparent.addExplosive((self.grandparent.player.rect.center), self.updated[0])
                self.grandparent.items[-1].drop()
            else: 
                self.grandparent.addItem((self.grandparent.player.rect.center), self.updated[0])
                self.grandparent.items[-1].drop()
            print(self.grandparent.items)
            
            self.removeItem() # make sure to spawn the item in the map
            self.interactDelay = 20
            print(self.updated)

        self.drawCarousel()

    def drawCarousel(self):
        # draw a square at the bottom of the screen
        pygame.draw.rect(self.grandparent.screen, (255,255,255), (0, self.grandparent.height - 100, self.grandparent.width, 100))
        
        # draw the items
        for i in range(len(self.updated)):
            item = self.updated[i]
            self.grandparent.screen.blit(pygame.image.load(os.path.join("sprites", item + ".png")), (i*100, self.grandparent.height - 75))
        
        pygame.display.update()