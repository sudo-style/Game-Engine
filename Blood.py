import pygame, sys, os, math
from pygame.locals import *

from CameraGroup import CameraGroup


class Blood:
    def __init__(self, texture_size):
        self.blood_surface = pygame.Surface(texture_size, pygame.SRCALPHA)
        self.blood_textures = []  # List of blood texture images
        self.max_health = 100

    def load_blood_textures(self):
        self.blood_textures.append(pygame.image.load(os.path.join('sprites', 'character', 'blood.png')).convert_alpha())

    def update_blood_effect(self, current_health):
        self.blood_surface.fill((0, 0, 0, 0))  # Clear the blood surface

        health_percentage = current_health / self.max_health

        if health_percentage <= 0.5:
            blood_intensity = 0.5  # Minimum blood intensity
        else:
            blood_intensity = 0.5 + (1 - health_percentage)  # Increase blood intensity as health decreases

        alpha_value = int(255 * blood_intensity)  # Convert blood intensity to alpha value (0-255)
        self.blood_surface.set_alpha(alpha_value)

        for blood_texture in self.blood_textures:
            x = 0
            y = 0
            self.blood_surface.blit(blood_texture, (x, y))

    def apply_blood_effect(self, original_texture):
        final_texture = original_texture.copy()
        try:
            final_texture.blit(self.blood_surface, (0, 0))
        except ValueError:
            new_surface = pygame.Surface(original_texture.get_size(), pygame.SRCALPHA)
            new_surface.fill((0, 0, 0, 0))
            new_surface.blit(self.blood_surface, (0, 0))
            return new_surface
        return final_texture


class Character(pygame.sprite.Sprite):
    def __init__(self, pos, group, name):
        super().__init__(group)
        self.image = pygame.image.load(os.path.join('sprites', 'character', name, name + '.png')).convert_alpha()
        self.ko_image = pygame.image.load(os.path.join('sprites','character', name, 'ko.png')).convert_alpha()
        self.naked_image = pygame.image.load(os.path.join('sprites','character', name, 'naked.png')).convert_alpha()
        self.blood_texture = pygame.image.load(os.path.join('sprites','character', 'blood.png')).convert_alpha()
        self.searchPos = pygame.Vector2()

        self.group = group
        self.offset = pygame.Vector2()  # New offset attribute

        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 3
        self.angle = 0
        oldCenter = self.rect.center
        self.oldCenter = oldCenter

        self.health = 100
        self.maxHealth = 100
        self.inputDelay = 0

        self.KO = False
        self.pos = pos
        self.searchPos = pygame.Vector2()

    def update(self):
        self.input()
        self.draw()
        self.rect.center += self.direction * self.speed
        pygame.display.update()
        self.inputDelay = max(self.inputDelay - 1, 0)
        self.pos = self.rect.center

    def input(self):
        self.movement()
        self.mouseRotation()

        # increase health if up is pressed
        keysPressed = pygame.key.get_pressed()
        if keysPressed[K_UP] and self.inputDelay <= 0:
            self.health += 10
            self.inputDelay = 20

        # decrease health if down is pressed
        if keysPressed[K_DOWN] and self.inputDelay <= 0:
            self.health -= 10
            self.inputDelay = 20

    def mouseRotation(self):
        # get the angle of the mouse and the center of the screen
        mouse_pos = pygame.mouse.get_pos()
        delta_x = mouse_pos[0] - self.rect.centerx + self.offset.x
        delta_y = mouse_pos[1] - self.rect.centery + self.offset.y
        self.angle = (180 / math.pi) * math.atan2(delta_y, delta_x)

    def draw(self):
        # rotate the image
        oldCenter = self.rect.center
        self.oldCenter = oldCenter
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter

        # have the blood effect translate with the character
        self.group.blood.update_blood_effect(self.health)
        self.image = self.group.blood.apply_blood_effect(self.image)

    def movement(self):
        keysPressed = pygame.key.get_pressed()
        if keysPressed[K_w]:
            self.direction.y -= 1
        if keysPressed[K_s]:
            self.direction.y += 1
        if keysPressed[K_a]:
            self.direction.x -= 1
        if keysPressed[K_d]:
            self.direction.x += 1

        # normalize vector
        if self.direction.length() > 0:
            self.direction.normalize_ip()
        self.rect.center += self.direction * self.speed

        self.direction = pygame.math.Vector2()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    blood_effect = Blood((148, 125))
    blood_effect.load_blood_textures()

    camera_group = pygame.sprite.Group()  # Use pygame.sprite.Group instead of CameraGroup
    player = Character((100, 100), camera_group, 'player')
    player.texture = pygame.image.load("sprites/character/player/player.png")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        camera_group.update()  # No need to modify this line
        player.offset = camera_group.sprites()[0].rect.center  # Set the offset based on camera_group
        player.update()
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
