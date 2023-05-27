import pygame
from pygame.locals import *
import os
import math

# Initialize pygame
pygame.init()

# Set up the screen
width = 1920
height = 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hitman")
clock = pygame.time.Clock()
FPS = 60

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

playerKeys = [K_LEFT, K_RIGHT, K_UP, K_DOWN]




class Character:
    def __init__(self, x, y, sprite):
        self.direction = 0
        self.original_sprite = pygame.image.load(os.path.join("sprites", sprite + ".png"))
        self.sprite = self.original_sprite.copy()
        self.rect = self.sprite.get_rect(center=(x, y))

    def draw(self):
        screen.blit(self.sprite, self.rect)

class Player(Character):
    def __init__(self, x, y, sprite='player'):
        super().__init__(x, y, sprite)

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)
    
    def rotate(self, angle):
        self.sprite = pygame.transform.rotate(self.original_sprite, -angle)
        self.rect = self.sprite.get_rect(center=self.rect.center)

    def update(self):
        speed = 3
        keysPressed = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keysPressed[K_w]: dy -= 1
        if keysPressed[K_s]: dy += 1
        if keysPressed[K_a]: dx -= 1
        if keysPressed[K_d]: dx += 1    
        
        if (dx != 0 and dy != 0): # normalize diagonal movement
            magnitude = math.sqrt(dx ** 2 + dy ** 2)
            dx /= magnitude
            dy /= magnitude
        dx *= speed
        dy *= speed
        self.move(dx, dy)

class NPC(Character):
    def __init__(self, x, y, sprite='clown'):
        super().__init__(x, y, sprite)
        self.states = ['path', 'investigate', 'sus', 'panic', 'dead']
        self.state = self.states[0]
        self.path = [(0, 0), (100, 0), (100, 100), (0, 100)]  # keeps looping through path to test

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

        # Update the player
        player.update()
        
        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate the angle between the player's position and the mouse position
        angle = math.degrees(math.atan2(mouse_y - player.rect.centery, mouse_x - player.rect.centerx))

        # Rotate the player sprite
        player.rotate(angle)

        clear()

        player.draw()

        draw()

    pygame.quit()

if __name__ == "__main__":
    main()
