import pygame
from pygame.locals import *
import os
import math

from Item import Item, Poison, Explosive
from CameraGroup import CameraGroup


class Inventory:
    def __init__(self, grandparent):
        self.grandparent = grandparent
        self.maxInventory = {'smg': 100, 'pistol': 69, 'sniper':100, 'gun':20}  
        self.inventory = []
        self.visible = True
        self.interactDelay = 0

    def addItem(self, Item):
        desiredName = Item.name
        
        for item in self.inventory:
            if item.name == desiredName:
                item.count += Item.count
                return
        self.inventory.append(Item)
    def currentItem(self):
        return self.inventory[0]
    
    def currentItemCount(self):
        return self.inventory[0].count

    def print(self):
        for item in self.inventory:
            print(f"{item.name} {item.count}")

    def removeCurrentItem(self):
        self.inventory[0].count -= 1
        if self.inventory[0].count <= 0:
            self.inventory.pop(0)

    def selectLeft(self):
        self.inventory = [self.inventory[-1]] + self.inventory[0:-1]
        
    def selectRight(self):
        self.inventory = self.inventory[1:] + self.inventory[:1]
    
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
        keeps = ['fiberWire', 'camera']
        return keep in keeps
        
    def shoot(self):
        # if not a gun don't shoot
        if not self.isCurrentItemGun(): return
        gun = self.currentItem()
        # if no ammo don't shoot
        if gun.count <= 0: return
        gun.count -= 1


        
def main():
    pygame.init()
    inventory = Inventory(None)
    group = pygame.sprite.Group()
    width = 1920
    height = 1080
    screen = pygame.display.set_mode((width, height))

    knife = Item((0,0), group, None, "knife")
    knife2 = Item((0,0), group, None, "knife")
    inventory.addItem(knife)
    inventory.addItem(knife2)
    


    inventory.addItem(Item((0,0), group, None, "gun"))

    
    inventory.selectLeft()
    inventory.removeCurrentItem()

    inventory.print()

    
if __name__ == "__main__":
    main()