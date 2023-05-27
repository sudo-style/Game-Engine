import pygame
from pygame.locals import *
import os
import math

# Initialize pygame
pygame.init()

# Set up the screen
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Top Down Shooter")
clock = pygame.time.Clock()
FPS = 60

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

playerKeys = [K_LEFT, K_RIGHT, K_UP, K_DOWN]




class Character:
    def __init__(self, sprite):
        self.direction = 0
        self.original_sprite = pygame.image.load(os.path.join("sprites", sprite + ".png"))

class Player(Character):
    def __init__(self, x, y, sprite='player'):
        super().__init__(sprite) 
        self.x = x
        self.y = y
        self.sprite = self.original_sprite.copy()
        self.rect = self.sprite.get_rect(center=(x, y))

    def draw(self):
        screen.blit(self.sprite, self.rect)

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)
    
    def rotate(self, angle):
        self.sprite = pygame.transform.rotate(self.original_sprite, -angle)
        self.rect = self.sprite.get_rect(center=self.rect.center)

def clear():
    screen.fill(black)    

def draw():
    clock.tick(FPS)
    pygame.display.flip()

def main():
    keepGoing = True

    player = Player(width // 2, height // 2)

    while keepGoing:
        for event in pygame.event.get():
            if event.type == QUIT:
                keepGoing = False

        keysPressed = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keysPressed[K_w]:
            dy -= 3
        if keysPressed[K_s]:
            dy += 3
        if keysPressed[K_a]:
            dx -= 3
        if keysPressed[K_d]:
            dx += 3

        player.move(dx, dy)

        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate the angle between the player's position and the mouse position
        angle = math.degrees(math.atan2(mouse_y - player.y, mouse_x - player.x))

        # Rotate the player sprite
        player.rotate(angle)

        clear()

        player.draw()

        draw()

    pygame.quit()

if __name__ == "__main__":
    main()
