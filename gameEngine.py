import pygame
from pygame.locals import *
import os
import math

from Inventory import Inventory


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

class Map:
    def __init__(self, name):
        self.name = name
        self.descritpion = ""
        self.targets = []
        self.rooms = []
        self.items = []
        self.npcs = []
        self.original_sprite = pygame.image.load(os.path.join("sprites", "map.png"))
        self.sprite = self.original_sprite.copy()
        self.player = Player(width/2, height/2)

    def update(self):
        # draw everything in the world
        self.draw()
    
    def addItem(self, item, pos = (0, 0)):
        self.items.append(Item(item, pos))
        

    def draw(self):
        # draw player
        #self.player.draw()

        # draw all items
        for item in self.items: item.draw()

        # draw all npcs
        for npc in self.npcs: npc.draw()


class Item:
    def __init__(self, name, pos):
        self.pos = pos
        self.name = name
        self.original_sprite = pygame.image.load(os.path.join("sprites", name + ".png"))
        self.sprite = self.original_sprite.copy()
        self.rect = self.sprite.get_rect(center=self.pos)

    def draw(self):
        screen.blit(self.sprite, (0, 0))

    def spawn(self):
        pass

class Character:
    def __init__(self, x, y, sprite):
        self.pos = (x, y)
        self.direction = 0
        self.original_sprite = pygame.image.load(os.path.join("sprites", sprite + ".png"))
        self.sprite = self.original_sprite.copy()
        self.rect = self.sprite.get_rect(center=self.pos)
        self.inventory = Inventory()

    def draw(self):
        screen.blit(self.sprite, self.rect)

    def spawn(self):
        pass

class Player(Character):
    def __init__(self, x, y, sprite='player'):
        super().__init__(x, y, sprite)

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)

    def rotate(self, angle):
        self.sprite = pygame.transform.rotate(self.original_sprite, -angle)
        self.rect = self.sprite.get_rect(center=self.rect.center)

    def update(self):
        # Movement
        speed = 3
        keysPressed = pygame.key.get_pressed()
        dx, dy = 0, 0

        # input for movement
        if keysPressed[K_w]: dy -= 1
        if keysPressed[K_s]: dy += 1
        if keysPressed[K_a]: dx -= 1
        if keysPressed[K_d]: dx += 1

        # normalize diagonal movement 
        if dx != 0 and dy != 0: 
            magnitude = math.sqrt(dx ** 2 + dy ** 2)
            dx /= magnitude
            dy /= magnitude
        dx *= speed
        dy *= speed
        self.move(dx, dy)

        # Rotation
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.degrees(math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx))
        self.rotate(angle)

        # Shooting
        # TODO: make this have a cooldown period instead of once per frame so you can't just hold down the mouse button
        if pygame.mouse.get_pressed()[0]:
            # make a line from player to mouse
            pygame.draw.line(screen, white, self.rect.center, (mouse_x, mouse_y), 2)
            pygame.display.flip()

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
    mission = Map("Hawkes Bay")

    # Load the background image
    background = pygame.image.load(os.path.join("sprites", "map.png"))

    # Create a camera rect centered around the player
    camera = pygame.Rect(0, 0, width, height)
    camera.center = mission.player.rect.center

    while keepGoing:
        for event in pygame.event.get():
            if event.type == QUIT:
                keepGoing = False

        # Update the player
        mission.player.update()

        # Update the camera position
        camera.center = mission.player.rect.center

        clear()

        # Draw the background image onto the screen
        screen.blit(background, (0, 0), camera)

        mission.player.draw()

        draw()

    pygame.quit()

if __name__ == "__main__":
    main()
