from GameObject import GameObject
from Character import Character
import pygame
import math
import copy


from random import randint

from Item import Flashbang

class NPC(Character):
	def __init__(self, pos, group, parent, name = "clown"):
		super().__init__(pos, group, parent, name)

		self.states = ['idle', 'patrol', 'alert', 'search', 'combat', 'ko', 'emetic', 'lethal']
		self.statesIndex = 1
		self.searchPos = pygame.Vector2()
		self.waypoints = [['eat', 0],
						  ['patrol', (200, 500)], 
						  ['patrol', (100, 100)], 
						  ['patrol', (200, 200)], 
						  ['idle', 200],
						  ['patrol', [parent.width/2, parent.height/2]]]
		self.originalWaypoints = copy.deepcopy(self.waypoints)  # Deep copy of original waypoints
		self.oxygen = 100
		self.KO = False
		maxStunTime = 100
		
	def breathing(self):
		self.oxygen = min(self.oxygen + 1, 100)

	def gettingSubdued(self):
		# oxygen decreases when getting strangled
		self.oxygen -= 2
		if self.oxygen <= 0: self.ko()

	def update(self):
		self.movementController() # controls movements of the NPC
		self.breathing()
		self.draw()
		if self.health <= 0: self.kill()
		self.pos = self.rect.center
	
	def getState(self):
		return self.states[self.statesIndex]

	def setState(self, state):
		if state in self.states:
			self.statesIndex = self.states.index(state)

	def setSearchPos(self, pos, radius):
		# random position within the radius
		radius = radius / 4 # closer but with small variation
		self.searchPos = pygame.Vector2(pos[0] + randint(-radius, radius), pos[1] + randint(-radius, radius))

	def nextWaypoint(self):
		print(self.waypoints)
		if self.lenWaypoints() > 0: self.waypoints.pop()
		else: self.waypoints = copy.deepcopy(self.originalWaypoints)

	def getWaypoint(self):
		return self.waypoints[-1]
	
	def lenWaypoints(self):
		return len(self.waypoints)
	
	def currentWaypoint(self): # returns the current waypoint
		return self.waypoints[self.lenWaypoints()-1]
	
	def movementController(self): # priority queue
		state = self.getState()
		# if knocked out, then can't do anything else
		if state == 'lethal':
			self.kill()
		if self.KO: return
		
		# if alerted, then go to the alert position
		if state == 'alert': 
			self.alert()
			print("ALERT")
			return	

		# if no special conditions are met, then this is the default state of the path of the NPC
		waypointState, waypointValue = self.getWaypoint()
		
		waypointState = self.getWaypoint()[0]
		#print("waypointState: " + waypointState)
		if waypointState == 'patrol': self.patrol()  # move towards the next waypoint
		if waypointState == 'search': self.search() # rotate to the direction 
		if waypointState == 'idle': self.idle()  # pause for self.waypoints[self.waypointIndex][1] frames
		if waypointState == 'dir': self.rotate() # rotate to the direction 
		if waypointState == 'eat': self.eat() # rotate to the direction
		
		# goes to the beginning of the path
		if self.lenWaypoints() == 0: self.waypoints = copy.deepcopy(self.originalWaypoints)  # Restore original waypoints using deep copy

	def rotate(self):
		angle = self.waypoints[-1][1]
		self.angle = angle
		self.image = pygame.transform.rotate(self.original_image, -self.angle)
		self.nextWaypoint()
	
	def ko(self):
		self.image = self.ko_image
		self.KO = True
		self.setState('ko')

	def eat(self):
		# find the closest food
		print("EATING")
		closestFood = None
		closestDistance = 30
		for food in self.parent.foods:
			distance = self.getDistanceTo(food)
			if distance < closestDistance:
				closestDistance = distance
				closestFood = food

		# will only eat 1 food or nothing
		if closestFood != None: closestFood.eat(self)
		self.nextWaypoint()

	def alert(self):
		# be idle for a couple seconds, then go to the position of the alert sound
		# make a new waypoint for the NPC
		print("alerted")
		self.waypoints = [['search', 200], ['dir', 45], ['search', 200], ['dir', 135], ['search', 200], ['patrol' , self.searchPos], ['idle', 200]]
		self.setState('patrol')

	def search(self):		
		# decreases the search time
		self.waypoints[-1][1] -= 1
		# if the NPC is close to the player then go into combat mode
		player = self.parent.player
		angleNPCtoPlayer = self.getDirectionTo(player)
		if self.isInLineOfSight(player, angleNPCtoPlayer, 10):
			print("Lets throw hands")
			self.setState('combat')
		if self.waypoints[-1][1] <= 0: self.nextWaypoint()
		
	def patrol(self):
		waypointState, waypointValue = self.getWaypoint()
		
		pos = GameObject(waypointValue)
		if self.getDistanceTo(pos) < self.speed: 
			print("NEXT WAYPOINT")
			self.nextWaypoint()
			return

		self.direction = pygame.math.Vector2(waypointValue[0] - self.rect.centerx, waypointValue[1] - self.rect.centery)
		if self.direction.length() > 0:
			self.direction.normalize_ip()
		self.rect.center += self.direction * self.speed
		# rotate the image to face the direction of the movement
		self.angle = (180 / math.pi) * math.atan2(self.direction.y, self.direction.x)
		self.image = pygame.transform.rotate(self.original_image, -self.angle)
		self.rect = self.image.get_rect(center = self.rect.center)
		# if the NPC is close the the search position, then go to the next waypoint

	def idle(self):
		self.waypoints[self.lenWaypoints()-1][1] -= 1
		# if the NPC is done being idle, then go to the next waypoint
		if self.waypoints[self.lenWaypoints()-1][1] <= 0: self.nextWaypoint()

		

class Guard(NPC):
	def __init__(self, pos, group, parent, name = "guard"):
		super().__init__(pos, group, parent, name)
		self.timeInAlertMode = 0

		self.waypoints = [['patrol', (0, 0)], 
						  ['patrol', (100, 100)], 
						  ['patrol', (200, 200)], 
						  ['idle', 200],
						  ['patrol', (30,30)]]
		self.originalWaypoints = copy.deepcopy(self.waypoints)  # Deep copy of original waypoints

	def combat(self):
		self.timeInAlertMode += 1

		if self.timeInAlertMode%4 == 0:
			# drop a flashbang
			print("flashbang")
		# try to follow the player and shoot at them
		player = self.parent.player
		angleNPCtoPlayer = self.getDirectionTo(player)
		if self.isInLineOfSight(player, angleNPCtoPlayer, 10):
			self.shoot()
			player.updateHealth()
		else:
			self.setState('alert')
			self.setSearchPos(player.rect.center, 100)
			self.alert()
		
		# if the player is close enough, then go into combat mode
		if self.getDistanceTo(player) < 100:
			if self.timeInAlertMode%4 == 0: print("Lets throw hands")
			self.setState('combat')
		else:
			self.setState('alert')
			self.setSearchPos(player.rect.center, 100)
			self.alert()

	def shoot(self):
		player = self.parent.player
		pygame.draw.line(self.parent.screen, (255, 255, 255), self.rect.center - self.group.offset, player.rect.center - player.group.offset, 2)
		pygame.display.update()
		player.health = max(0, player.health - 10)
		# play sound of gun
		# play gun.wav
		pygame.mixer.music.load('sounds/gun.wav')
		pygame.mixer.music.play(0)
		
		

	def movementController(self): # priority queue
		state = self.getState()
		
		# if knocked out, then can't do anything else
		if self.KO: return
		
		# if alerted, then go to the alert position
		if state == 'alert': 
			self.alert()
			print("ALERT")
			return

		if state == 'combat':
			self.combat()
			print("COMBAT")
			return

		# if no special conditions are met, then this is the default state of the path of the NPC
		waypointState, waypointValue = self.getWaypoint()
		
		waypointState = self.getWaypoint()[0]
		#print("waypointState: " + waypointState)
		if waypointState == 'patrol': self.patrol()  # move towards the next waypoint
		if waypointState == 'search': self.search() # rotate to the direction 
		if waypointState == 'idle': self.idle()  # pause for self.waypoints[self.waypointIndex][1] frames
		if waypointState == 'dir': self.rotate() # rotate to the direction 
		
		# goes to the beginning of the path
		if self.lenWaypoints() == 0: self.waypoints = copy.deepcopy(self.originalWaypoints)  # Restore original waypoints using deep copy