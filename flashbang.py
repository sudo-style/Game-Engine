import pygame, sys, os, math
from pygame.locals import *





class Flashbang():
    

    def __init__(self, screen, width, height):
        self.whiteSquare = pygame.Rect((0, 0, width, height))
        self.on = False
        self.timer = 0

    def trigger(self):
        self.on = True

    def update(self):
        # once the flashbang is triggered, it will stay on for 1 second
        if self.on:
            self.timer += 1
            if self.timer >= 60:
                self.on = False
                self.timer = 0
            print(self.timer)


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