import pygame
from pygame.locals import *
import os
import math

from Item import Item
from Character import Player, NPC
from Map import Map

def main():
    keepGoing = True
    pygame.init()
    width = 1920
    height = 1080
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hitman")
    clock = pygame.time.Clock()
    fps = 60
    mission = Map("Hawkes Bay", width, height, screen, clock, fps)

    mission.addItem("knife", (100, 100))
    
    while keepGoing:
        for event in pygame.event.get():
            if event.type == QUIT:
                keepGoing = False

        mission.update()
        
        
    pygame.quit()

if __name__ == "__main__":
    main()
