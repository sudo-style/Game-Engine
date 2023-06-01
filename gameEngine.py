import pygame, sys, os, math
from pygame.locals import *


from Map import Map
from CameraGroup import CameraGroup

def main():
    pygame.init()
    width = 1920
    height = 1080
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hitman")
    clock = pygame.time.Clock()
    fps = 60
    camera_group = CameraGroup()
    mission = Map("Hawkes Bay", width, height, screen, clock, fps, camera_group)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        camera_group.update()
        camera_group.custom_draw(mission.player) # this will focus on the player
        mission.clock.tick(mission.fps)

if __name__ == "__main__":
    main()
