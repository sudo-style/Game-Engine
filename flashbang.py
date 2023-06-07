import pygame
import sys
import numpy as np
from pygame.locals import *

class Flashbang:
    def __init__(self, screen, width, height):
        #self.whiteSquare = pygame.Rect((0, 0, width, height))
        self.on = False
        self.timer = 0
        self.width = width
        self.height = height
        self.screen = screen

    def trigger(self, stunTime=300):
        self.on = True
        self.timer = stunTime

        # Get a freeze frame of the current screen
        self.freezeFrame = pygame.Surface((self.width, self.height))

    def update(self):
        # Once the flashbang is triggered, it will stay on for the specified time
        if self.on:
            self.timer -= 1
            if self.timer <= 0:
                self.on = False
                self.timer = 0
            print(self.timer)

    def brightnessFunction(self, x):
        # This function returns the brightness of the flashbang at a given distance x
        if 0 <= x <= 20: return 1 - np.exp(-10 * x)
        elif 20 <= x <= 100: return 1
        elif 100 <= x <= 400: return 1 - 0.005 * (x - 100)
        else: return 0

    def draw(self):
        if self.on:
            brightness = self.brightnessFunction(self.timer/60)
            color = (int(brightness * 255), int(brightness * 255), int(brightness * 255))
            pygame.draw.rect(self.screen, color, self.screen.get_rect())

def main():
    pygame.init()
    width = 1920
    height = 1080
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Flashbang")
    clock = pygame.time.Clock()
    fps = 60
    flashbang = Flashbang(screen, width, height)
    
    triggerTest = 100

    while True:
        # Trigger the flashbang
        triggerTest = max(triggerTest-1, 0)
        if triggerTest <= 0:
            flashbang.trigger()
            triggerTest = 1000
            
        # Draw the flashbang to the screen
        screen.fill((0, 0, 0))
        flashbang.draw()
        flashbang.update()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(fps)

if __name__ == "__main__":
    main()
