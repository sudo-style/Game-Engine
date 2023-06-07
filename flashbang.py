import pygame, sys, os, math, np
from pygame.locals import *

class Flashbang():
    def __init__(self, width, height):
        self.whiteSquare = pygame.Rect((0, 0, width, height))
        self.on = False
        self.timer = 0

    def trigger(self, stunTime = 100):
        self.on = True
        self.timer = stunTime

        # get a freeze frame of the current screen
        self.freezeFrame = pygame.Surface((self.width, self.height))

    def update(self):
        # once the flashbang is triggered, it will stay on for 1 second
        if self.on:
            self.timer -= 1
            if self.timer <= 0:
                self.on = False
                self.timer = 0
            print(self.timer)

    def brightnessFunction(x):
        # this function will return the brightness of the flashbang at a given distance, and time
        if 0 <= x <= 5: return 1 - np.exp(-10 * x)
        elif 5 <= x <= 100: return 1
        elif 100 <= x <= 400: return 1 - 0.005 * (x - 100)
        else: return 0

def main():
    pygame.init()
    width = 1920
    height = 1080
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Flashbang")
    clock = pygame.time.Clock()
    fps = 60
    flashbang = Flashbang(screen, width, height)
    flashbang.trigger()

    while True:
        # draw the flashbang to the screen
        screen.fill((0, 0, 0))
        
        if flashbang.on: pygame.draw.rect(screen, (255, 255, 255), flashbang.whiteSquare)
        flashbang.update()

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(fps)

if __name__ == "__main__":
    main()