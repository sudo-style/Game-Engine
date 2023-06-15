import pygame, os, math
from pygame.locals import *
from GameObject import GameObject

class Item(pygame.sprite.Sprite, GameObject):
	def __init__(self, pos, group, parent, name, count=1):
		super().__init__(group)
		GameObject.__init__(self, pos)
		self.image = pygame.image.load(os.path.join("sprites", 'items', name + ".png")).convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.parent = parent
		self.name = name
		self.pickUpTime = 0
		self.count = count
		self.velocity = 0 
		self.direction = pygame.math.Vector2()
		
	def interact(self):
		pass

	def drop(self):
		print(f"dropped {self.name}")
		pass

	def pickUp(self):
		self.pickUpTime = max(self.pickUpTime - 1, 0)
		if self.pickUpTime > 0: return

		if self.parent.player.rect.colliderect(self.rect) and pygame.key.get_pressed()[K_f]:
			self.parent.player.inventory.addItem(self)
			self.kill()

	def throw(self, direction):
		self.direction = direction
		print(f"throwing {self.name} at {self.direction} with velocity {self.velocity}")
		self.velocity = 20
		self.direction = pygame.math.Vector2(self.parent.player.direction)

	def update(self):
		self.pickUp()
		if type(self) == RemoteExplosive:
			print(self.pos, self.direction, self.velocity)
			print(math.cos(self.direction[0]), math.sin(-self.direction[1]))

		# move the item in the direction of its velocity
		self.subtractVelocity(1) # todo find sweet spot
		
		# players direction adds up to 1 so need to change to degrees
		degrees = (math.radians(self.direction[0]), math.radians(self.direction[1]))
		self.pos = (self.pos[0] + math.cos(degrees[0]) * self.velocity, 
	    			self.pos[1] + math.sin(degrees[1]) * self.velocity)

		self.rect.center = self.pos
		
class Explosive(Item):
	def __init__(self, pos, group, parent, name = "bomb", direction = 1, velocity = 1):
		super().__init__(pos, group, parent, name)
		self.damage = 100
		self.damageRadius = 100
		self.soundRadius = 500

		self.fuseTime = 200
		self.boolTriggered = False
		
		# sound
		self.sound = pygame.mixer.Sound(os.path.join("sounds", "grenade.wav"))
		self.fuse = pygame.mixer.Sound(os.path.join("sounds", "fuse.mp3"))
	
	def drop(self):
		pass

	def ifTriggered(self):
		pass

	def update(self):
		# trigger the explosive if the player is close enough
		super().update()
		self.pickUp()
		self.ifTriggered()
	
	def alertNPCs(self):
		for npc in self.parent.npcs:
			# check if the npc is in the radius of sound
			distance = self.getDistanceTo(npc)
			if (distance <= self.soundRadius):
				npc.setState('alert')
				npc.setSearchPos(self.rect.center, self.soundRadius)
			if (distance <= self.damageRadius):
				npc.health -= self.damage

	def explode(self):
		self.sound.play()

		# draw the damage and sound radius
		pygame.draw.circle(self.parent.screen, (255,0,0), self.rect.center, self.damageRadius)
		pygame.draw.circle(self.parent.screen, (0,0,255), self.rect.center, self.soundRadius, 1)
		pygame.display.update()

		# check any characters in the sound radius
		self.alertNPCs()

		# explode explosives in the radius
		for explosive in self.parent.items:
			# check if the class is an explosive
			if not isinstance(explosive, Explosive): continue
			if explosive == self: break
			if (self.rect.colliderect(explosive.rect)):
				self.sound.play()
				explosive.explode()

		# remove the explosive from the map
		self.kill()

class Grenade(Explosive):
	def __init__(self, pos, group, parent, name = 'grenade', direction = 1, velocity = 1):
		super().__init__(pos, group, parent, 'grenade')
	
	def drop(self):
		print(f"dropped Explosive {self.name}")
		self.boolTriggered = True
		self.fuse.play()
	
	def ifTriggered(self):
		if not self.boolTriggered: return
		self.fuseTime -= 1
		if (self.fuseTime <= 0): self.explode()

class RemoteExplosive(Explosive):
	def __init__(self, pos, group, parent, name = 'remote explosive', count = 1, direction = 1, velocity = 1):
		super().__init__(pos, group, parent, 'remote explosive')
			 
	def drop(self):
		# add a trigger button to the players inventory
		# if they press the trigger, then the original explosive will explode
		trigger = Trigger((self.rect.center), self.parent.camera_group, self.parent, self, 'trigger')
		self.parent.player.inventory.addItem(trigger)
		pass

	def ifTriggered(self):
		
		#self.explode()
		pass

class Trigger(Item): # this will only exist in the player inventory, they can't drop it, once they use it it will be removed from the inventory
	def __init__(self, pos, group, parent, explosiveParent, name = "trigger", direction = 1, velocity = 1):
		super().__init__(pos, group, parent, name)
		self.explosiveParent = explosiveParent

	def drop(self):
		pass

	def update(self):
		self.kill()

	def interact(self):
		self.explosiveParent.explode()
		self.parent.player.inventory.removeItem(self)

# player can poison food
# NPC can move, and eat food
class Food(Item):
	def __init__(self, pos, group, parent, name = "food", direction = 1, velocity = 1):
		super().__init__(pos, group, parent, name)
		self.poisonStates = ['none', 'ko', 'lethal', 'emetic']
		self.poisonState = 0

	def getPoisonState(self):
		return self.poisonStates[self.poisonState]
	
	def gettingPoisoned(self, state):
		print('food is poisoned')
		self.poisonState = self.poisonStates.index(state)
	
	def eat(self, target):
		# if the food was poisoned then the target will be poisoned
		if (self.poisonStates[self.poisonState] == 'none'):
			print("MMM, that was good")
			self.kill()
			return
		print(f"{target.name} was poisoned")
		target.setState(self.poisonStates[self.poisonState])
		if self.getPoisonState()== 'ko': target.ko()
		self.kill()

	def update(self):
		self.pickUp()
		
class Poison(Item):
	def __init__(self, pos, group, parent, name = 'knockout pill', poisonState = "ko", poisonType = 'pill'):
		super().__init__(pos, group, parent, name)
		self.name = name
		self.poisonType = poisonType
		self.poisonStates = poisonState
		self.poisonState = 0
		self.enabled = True
		self.poisoned = False
		self.timer = 100

	def update(self):
		if self.poisoned: 
			self.timer = max(self.timer-1, 0)
		
		if self.timer == 0:
			self.enabled = True
			if self.poisoned: self.kill()
			self.timer = 100

		if self.enabled: self.pickUp()

	def drop(self):
		self.poisoned = False
		
		if self.poisonType == 'injection':
			touchingNPCs = self.rect.collideobjectsall(self.parent.npcs)
			for npc in touchingNPCs: 
				self.enabled = False
				self.poisoned = True
				npc.ko()
				print("KNOCKOUT\t\tKNOCKOUT")
		
		if self.poisonType == 'pill':
			touchingFoods = self.rect.collideobjectsall(self.parent.foods)
			for food in touchingFoods:
				self.enabled = False
				self.poisoned = True
				food.gettingPoisoned('ko')
				print(f"poisoned {food.name}")
		# when dropped it will try to poison the colliders either food or NPC 
		# after 3 seconds it will disappear, showing that it has infected that area
		
	def poison(self, target):
		print(f"{target.name} was poisoned")
		target.poisoned(self.poisonState)
		self.kill()

class Gun(Item):
	def __init__(self, pos, group, parent, name, count, fireRate = 10, direction = 1, velocity = 1):
		super().__init__(pos, group, parent, name, count)
		self.fireRate = fireRate
		self.sound = pygame.mixer.Sound(os.path.join("sounds", "gun.WAV"))
	
class Camera(Item):
	def __init__(self, pos, camera_group, parent, name, count = 1, direction = 1, velocity = 1):
		super().__init__(pos, camera_group, parent, name)
		self.camera_group = camera_group
		
	def interact(self):
		self.camera_group.takeScreenshot(self.parent.player)

class Exit(Item):
	def __init__(self, pos, group, parent, name = 'exit'):
		super().__init__(pos, group, parent, name)

	def pickUp(self):
		pass

	def update(self):
		# check if the player is touching the exit
		if self.rect.colliderect(self.parent.player.rect): 
			# check if all of the NPC's are dead
			for npc in self.parent.npcs:
				print(npc.health)
			print("\n")
			for npc in self.parent.npcs:
				print(npc.health)
				if npc.health > 0: return

			# todo make this go to see the score
			self.kill()
				