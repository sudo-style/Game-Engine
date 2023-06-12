import pygame 
from pygame.locals import *
import os
#from Inventory import Inventory
from GameObject import GameObject
import math 
import copy
from random import randint

white = (255, 255, 255)
class Character(pygame.sprite.Sprite, GameObject):
	def __init__(self, pos, group, parent, name):
		super().__init__(group)
		self.name = name
		self.image = pygame.image.load(os.path.join('sprites', 'character', name, name + '.png')).convert_alpha()
		self.ko_image = pygame.image.load(os.path.join('sprites','character', name, 'ko.png')).convert_alpha()
		self.naked_image = pygame.image.load(os.path.join('sprites','character', name, 'naked.png')).convert_alpha()
		self.blood_texture = pygame.image.load(os.path.join('sprites','character', 'blood', 'blood0.png')).convert_alpha()
		
		self.original_image = self.image.copy()
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2()
		self.speed = 3
		self.angle = 0
		oldCenter = self.rect.center
		self.oldCenter = oldCenter
		self.group = group
		self.parent = parent
		self.health = 100
		self.maxHealth = 100

		self.suitName = name
		self.pos = pos

	def updateHealth(self):
		blood_textures = {
			range(0, 25): 'blood3.png',
			range(26, 51): 'blood2.png',
			range(51, 76): 'blood1.png',
			range(76, 100): 'blood0.png'
		}

		for health_range, blood_texture_name in blood_textures.items():
			if self.health in health_range:
				self.blood_texture = pygame.image.load(os.path.join('sprites', 'character', 'blood', blood_texture_name)).convert_alpha()
				break

	def draw(self):
		# takes the original image, adds the blood texture, and rotates it
		transformed_image = pygame.Surface(self.original_image.get_size(), pygame.SRCALPHA)
		transformed_image.blit(self.original_image, (0, 0))
		transformed_image.blit(self.blood_texture, (0, 0))
		rotated_image = pygame.transform.rotate(transformed_image, -self.angle)
		self.image = rotated_image
		self.rect = self.image.get_rect(center=self.rect.center)


