#!/usr/bin/python3

# Represents an asteroid in the game.
# By BEN COLLINS

from canvas.canvas import *
from consts import *
from random import *
import math
			
class Asteroid:
	
	def __init__(self, game):
		self.game = game

		# Calculate initaial size of asteroid.
		self.size = ASTEROID_SIZE + ASTEROID_SIZE_RANGE * random()
		x = (random() * 2 - 1) * MAP_SIZE
		y = (random() * 2 - 1) * MAP_SIZE

		# Create asteroid object and add it to the canvas.
		self.shape = Rect(x, y, self.size, self.size, ASTEROID_COLOR, layer = "content")
		self.game.canvas.add(self.shape)
		
		# Calculate initial velocity of asteroid.
		theta = randint(0, 360)
		self.vx = math.cos(theta) * ASTEROID_SPEED
		self.vy = math.sin(theta) * ASTEROID_SPEED
		
	def update(self, player, enemies):
		# Move the asteroid according to its velocity.
		self.collideWithPlayer(player)
		self.collideWithEnemy(enemies)
		self.bounceOfEdges()
		self.shape.x += self.vx
		self.shape.y += self.vy
		
	def collideWith(self, obj):
		# Check if the distants between the object and asteroid is greater than there sizes.
		xdist = abs(self.shape.x - obj.shape.x)
		ydist = abs(self.shape.y - obj.shape.y)
		xcheck = xdist * 2 < self.size + PLAYER_SIZE
		ycheck = ydist * 2 < self.size + PLAYER_SIZE

		if xcheck and ycheck:
			# Move the velocity of one object to the next.
			if xdist > ydist:
				temp = obj.vx
				obj.vx = self.vx
				self.vx = temp
			else:
				temp = obj.vy
				obj.vy = self.vy
				self.vy = temp

	def collideWithPlayer(self, player):
		self.collideWith(player)
				
	def collideWithEnemy(self, enemies):
		for enemy in enemies:
			self.collideWith(enemy)

	def bounceOfEdges(self):
		# Check for collision with each of the walls an flip the velocity of the correct axis.
		if self.shape.x + self.size / 2 > MAP_SIZE:
			self.shape.x = MAP_SIZE - self.size / 2
			self.vx *= -0.5
		if self.shape.x - self.size / 2 < -MAP_SIZE:
			self.shape.x = -MAP_SIZE + self.size / 2
			self.vx *= -0.5
		if self.shape.y + self.size / 2 > MAP_SIZE:
			self.shape.y = MAP_SIZE - self.size / 2
			self.vy *= -0.5
		if self.shape.y - self.size / 2 < -MAP_SIZE:
			self.shape.y = -MAP_SIZE + self.size / 2
			self.vy *= -0.5

	def hit(self):
		# If hit by a bullet decrese size.
		self.size -= 5
		self.shape.w = self.size
		self.shape.h = self.size

		# If too small respawn asteroid in a new loaction.
		if self.size < ASTEROID_SIZE:
			self.shape.x = (random() * 2 - 1) * MAP_SIZE
			self.shape.y = (random() * 2 - 1) * MAP_SIZE
			self.size = ASTEROID_SIZE + ASTEROID_SIZE_RANGE * random()