from canvas.canvas import *
from consts import *
from random import *
import math
			
class Asteroid:
	
	def __init__(self, game):
		self.size = ASTEROID_SIZE + ASTEROID_SIZE_RANGE * random()
		x = (random() * 2 - 1) * MAP_SIZE
		y = (random() * 2 - 1) * MAP_SIZE
		self.shape = Rect(x, y, self.size, self.size, ASTEROID_COLOR, layer = "content")
		self.game = game
		self.game.canvas.add(self.shape)
		
		theta = randint(0, 360)
		self.vx = math.cos(theta) * ASTEROID_SPEED
		self.vy = math.sin(theta) * ASTEROID_SPEED
		
	def update(self, player, enemies):
		self.shape.x += self.vx
		self.shape.y += self.vy
		
		self.collideWithPlayer(player)
		self.collideWithEnemy(enemies)
		self.bounceOfEdges()
		
	def collideWith(self, obj):
		xdist = abs(self.shape.x - obj.shape.x)
		ydist = abs(self.shape.y - obj.shape.y)
		xcheck = xdist * 2 < self.size + PLAYER_SIZE
		ycheck = ydist * 2 < self.size + PLAYER_SIZE

		if xcheck and ycheck:	
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
		self.size -= 5
		self.shape.w = self.size
		self.shape.h = self.size
		if self.size < ASTEROID_SIZE:
			self.shape.x = (random() * 2 - 1) * MAP_SIZE
			self.shape.y = (random() * 2 - 1) * MAP_SIZE
			self.size = ASTEROID_SIZE + ASTEROID_SIZE_RANGE * random()