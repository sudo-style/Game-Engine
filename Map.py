import pygame
from pygame.locals import *
import os
import math
from random import randint

from Item import Item, Explosive, Food, Poison, Gun, Camera, Grenade, RemoteExplosive, Exit
from Character import Character
from Player import Player
from NPC import NPC, Guard
from GameObject import GameObject


class Map:
	def __init__(self, name, width, height, screen, clock, fps, camera_group):
		self.name = name
		self.description = ""
		self.targets, self.rooms, self.items, self.npcs, self.foods = [], [], [], [], []
		self.original_sprite = pygame.image.load(os.path.join("sprites", 'map', "GroundFloor.png"))
		self.sprite = self.original_sprite.copy()
		
		self.width = width
		self.height = height
		self.screen = screen
		self.clock = clock
		self.fps = fps
		self.camera_group = camera_group

		# adding food to the map
		self.addFood((200,500), 'apple')

		self.addItem((0,0),'fiberWire')

		# add player to the map
		self.player = Player((width/2, height/2), self.camera_group, self, 'player')

		self.addItem((width/2, height/2), 'knife')
		
		# adding an npc to the map
		self.addExplosive((width/2, height/2))
		self.addGun((width/2-200, height/2+ 100), 'gun', 5, 20)
		
		# add poison to the map
		self.addPoison((300, 600), 'knockout pill', 'ko', 'pill')
		self.addPoison((400, 600), 'lethal pill', 'lethal', 'pill')
		self.addPoison((500, 600), 'knockout injection','ko', 'injection')

		self.addCamera((700,700))


		self.addNPC((width/2, height/2), 'clown')
		self.addGuard((width, height/2), 'guard')
		self.addGuard((width/2 + 200, height/2 + 200), 'guard')
		self.addGrenade((width/2 - 200, height/2 - 200))

		self.addRemoteExplosive((width/2 - 300, height/2 - 300))
		self.addExit((width/2 - 500, height/2 - 500))
	
	def addRemoteExplosive(self, pos):
		remoteExplosive = RemoteExplosive(pos, self.camera_group, self)
		self.items.append(remoteExplosive)

	def addGrenade(self, pos):
		grenade = Grenade(pos, self.camera_group, self)
		self.items.append(grenade)
	
	def addExplosive(self, pos, name = 'bomb'):
		explosive = Explosive(pos, self.camera_group, self, name)
		self.items.append(explosive)

	def addItem(self, pos, name, count = 1):
		item = Item(pos, self.camera_group, self, name, count)
		self.items.append(item)

	def addNPC(self, pos, name):
		npc = NPC(pos, self.camera_group, self, name)
		self.npcs.append(npc)

	def addGuard(self, pos, name):
		guard = Guard(pos, self.camera_group, self, name)
		self.npcs.append(guard)

	def addFood(self, pos, name):
		food = Food(pos, self.camera_group, self, name)
		self.foods.append(food)

	def addPoison(self, pos, name, state, type):
		poison = Poison(pos, self.camera_group, self, name, state, type)
		self.items.append(poison)

	def addGun(self, pos, name, count, fireRate):
		gun = Gun(pos, self.camera_group, self, name, count, fireRate)
		self.items.append(gun)

	def addCamera(self, pos):
		camera = Camera(pos, self.camera_group, self, 'camera')
		self.items.append(camera)

	def addExit(self, pos):
		exit = Exit(pos, self.camera_group, self, 'exit')
		self.items.append(exit)