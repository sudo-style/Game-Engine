import pygame
from pygame.locals import *
import os
import math


from Item import Item, Poison, Explosive, Gun, Food
from CameraGroup import CameraGroup



class Inventory:
    def __init__(self, grandparent):
        self.grandparent = grandparent
        self.inventory = []
        self.visible = False
        self.interactDelay = 0

    def print(self):
        for item in self.inventory:
            print(f"{item.name} {item.count}")
    
    def removeItem(self, obj):
        self.inventory.remove(obj)

    def addItem(self, Item):
        desiredName = Item.name
        # remove the item from the inventory array
        for item in self.inventory:
            if item.name == desiredName:
                Item.count += item.count
                self.inventory.remove(item)
                print('removed item')
        
        # this is done so items are added to the front of the array
        self.inventory = [Item] + self.inventory
        self.limitInventoryToMax(desiredName)

    def limitInventoryToMax(self, name):
        if name not in self.maxInventory(): return
        for item in self.inventory:
            if item.name == name:
                item.count = min(item.count, self.maxInventory()[name])    

    def dropItem(self, pos):
        currentItem = self.currentItem()
        # don't drop keeps
        if self.isCurrentItemKeep(): return    
        item = type(currentItem)(pos, self.grandparent.camera_group, self.grandparent, currentItem.name)
        self.grandparent.items.append(item)
        self.grandparent.items[-1].drop()
        self.inventory.remove(currentItem)
        return

    def currentItem(self):
        return self.inventory[0]

    def currentItemCount(self):
        return self.inventory[0].count

    def selectLeft(self):
        if len(self.inventory) == 0: return
        self.inventory = [self.inventory[-1]] + self.inventory[0:-1]
        
    def selectRight(self):
        if len(self.inventory) == 0: return
        self.inventory = self.inventory[1:] + self.inventory[:1]

    def maxInventory(self):
        return {'smg': 100, 'pistol': 69, 'sniper':100, 'gun':20}  
    
    def isCurrentItemGun(self):
        gun = self.currentItem().name
        guns = ['smg', 'pistol', 'sniper', 'gun']
        return gun in guns
    
    def isCurrentItemPoison(self):
        poison = self.currentItem().name
        poisons = ['ko', 'lethal', 'emetic']
        return poison in poisons
    
    def isCurrentItemExplosive(self):
        explosive = self.currentItem().name
        explosives = ['bomb', 'tnt', 'grenade', 'rubber duck']
        return explosive in explosives
    
    def isCurrentItemKeep(self):
        keep = self.currentItem().name
        keeps = ['camera', 'trigger']
        return keep in keeps

    def shoot(self):
        # if not a gun don't shoot
        if not self.isCurrentItemGun(): return
        gun = self.currentItem()
        # if no ammo don't shoot
        if gun.count <= 0: return
        gun.count -= 1

    def drawCount(self):
        if len(self.inventory) == 0: return
        item = self.currentItem()
        font = pygame.font.SysFont(None, 30)
        countText = font.render(str(item.count), True, (255,255,255))
        nameText = font.render(str(item.name), True, (255,255,255))
        self.grandparent.screen.blit(countText, (0,0))
        self.grandparent.screen.blit(nameText, (90,60))
        self.grandparent.screen.blit(item.image, (0, 30))
        
    def drawCarousel(self):
        pygame.draw.rect(self.grandparent.screen, (255,255,255), (0, self.grandparent.height - 100, self.grandparent.width, 100))
        for i in range(len(self.inventory)):
            item = self.inventory[i]
            self.grandparent.screen.blit(pygame.image.load(os.path.join('sprites','items', item.name + '.png')), (i*100, self.grandparent.height - 75))

    def update(self):
        self.interactDelay = max(0, self.interactDelay - 1)
        keysPressed = pygame.key.get_pressed()
        
        self.drawCount()

        # v toggles visibility
        if keysPressed[K_v] and self.interactDelay == 0:
            self.visible = not self.visible
            self.interactDelay = 10
        
        if keysPressed[K_LEFT] and self.interactDelay == 0:
            self.selectLeft()
            self.interactDelay = 10
        if keysPressed[K_RIGHT] and self.interactDelay == 0:
            self.selectRight()
            self.interactDelay = 10
            

        if not self.visible: return
        # left and right arrows to switch items
        