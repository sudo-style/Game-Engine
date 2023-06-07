import pygame
import sys
import numpy as np
from pygame.locals import *

class Flashbang:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.whiteoutSurface = pygame.Surface((width, height))
        self.whiteoutSurface.fill((255, 255, 255))
        self.whiteoutSurface.set_alpha(0)  # Initial alpha value of 0
        self.on = False
        self.timer = 0
        self.freezeFrame = pygame.image.load("freezeFrame.png")

    def trigger(self, stunTime=200):
        self.on = True
        self.timer = stunTime
        self.stunTime = stunTime
        print("triggered")

    def update(self):
        if self.on:
            self.timer -= 1
            if self.timer <= 0:
                self.on = False
                self.timer = 0

    def brightnessFunction(self):
        animationPercentage = 1 - self.timer / self.stunTime
        if animationPercentage <= 0.01: return animationPercentage / 0.01  # Rapidly ramp up from 0 to 1
        elif 0.01 < animationPercentage <= 0.2: return 1  # Hold at 1 for 20% of the animation
        else: return 1 - (animationPercentage - 0.2) / 0.4  # Slowly fade from 1 to 0


    def afterimageBrightnessFunction(self):
        animationPercentage = self.timer / self.stunTime
        if animationPercentage <= 0.1: return 0  # Hold at 0 for the first 10% of the animation
        elif 0.1 < animationPercentage <= 0.4: return (animationPercentage - 0.1) / 0.3 * 0.33  # Ramp up to 33%
        else: return 0.33 - (animationPercentage - 0.4) / 0.6 * 0.33  # Slowly fade from 33% to 0

    def draw(self):
        if self.on:
            # Calculate brightness for both flashbang and afterimage
            flashbangBrightness = self.brightnessFunction()
            afterimageBrightness = self.afterimageBrightnessFunction()

            # Determine the alpha values based on the brightness values
            flashbangAlpha = int(flashbangBrightness * 255)
            afterimageAlpha = int(afterimageBrightness * 255)

            # Set alpha values for the whiteout surface and the afterimage surface
            self.whiteoutSurface.set_alpha(flashbangAlpha)
            self.freezeFrame.set_alpha(afterimageAlpha)

            # Draw the whiteout surface to cover the entire screen
            self.screen.blit(self.whiteoutSurface, (0, 0))

            # Draw the freeze frame afterimage on top of the whiteout surface
            self.screen.blit(self.freezeFrame, (0, 0))

def main():
    pygame.init()
    width = 1920
    height = 1080
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Flashbang")
    clock = pygame.time.Clock()
    fps = 60
    flashbang = Flashbang(screen, width, height)
    timer = 200


    while True:
        timer -= 1
        if timer <= 0:
            flashbang.trigger()
            timer = 1000
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
