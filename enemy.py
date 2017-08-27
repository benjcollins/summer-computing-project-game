#!/usr/bin/python3

from canvas.canvas import *
from consts import *
from bullet import *
from random import *
import math

class Enemy:

	def __init__(self, game, speed, health):
		self.game = game
		self.speed = speed
		self.max_health = health
		self.health = health
		self.vx = 0
		self.vy = 0

		# Calculate intital position randomly.
		x = (random() * 2 - 1) * MAP_SIZE
		y = (random() * 2 - 1) * MAP_SIZE

		# Create the shape and add it too the canvas.
		self.shape = Rect(x, y, PLAYER_SIZE, PLAYER_SIZE, DAMAGE_COLOR, layer = "content")
		self.game.canvas.add(self.shape)

		# Calculate position of the health bar create the shape and add it to the canvas.
		right = x - PLAYER_SIZE / 2
		top = y - PLAYER_SIZE / 2
		self.health_bar = Rect(right, top, PLAYER_SIZE, PLAYER_SIZE, HEALTH_COLOR, layer = "content", flow = "right")
		self.game.canvas.add(self.health_bar)

	def update(self, asteroids, player):
		self.moveEnemy(player)
		self.bounceOfEdges()
		self.collideWithPlayer(player)

		# Update the shape position according to the velocity.
		self.shape.x += self.vx
		self.shape.y += self.vy
		self.updateHealthBar()
		
	def collideWithPlayer(self, player):
		# Check if the distants between the player and enemy is greater than there sizes.
		xdist = abs(self.shape.x - player.shape.x)
		ydist = abs(self.shape.y - player.shape.y)
		xcheck = xdist < PLAYER_SIZE
		ycheck = ydist < PLAYER_SIZE
		
		if xcheck and ycheck:
			# If this is true remove the enemy and notify the player that it was hit.
			player.damage()
			self.die()

	def updateHealthBar(self):
		# Make sure the health bar is alway ontop of the enemy.
		self.health_bar.x = self.shape.x - PLAYER_SIZE / 2
		self.health_bar.y = self.shape.y - PLAYER_SIZE / 2
		self.health_bar.w = PLAYER_SIZE / self.max_health * self.health

	def moveEnemy(self, player):
		# Use pythagoras theorm to calculate the distance between the enemy and player.
		diffx = player.shape.x - self.shape.x
		diffy = player.shape.y - self.shape.y
		length = math.sqrt(diffx ** 2 + diffy ** 2)

		# Create a scale factor with the enemys max speed and create an ideal velocity for enemy.
		scale = ENEMY_MAX_SPEED / length
		vx = diffx * scale
		vy = diffy * scale
		
		# Try to get as close to that vector as possible.
		if vx > self.vx:
			self.vx += self.speed
		else:
			self.vx -= self.speed
			
		if vy > self.vy:
			self.vy += self.speed
		else:
			self.vy -= self.speed

	def hit(self, player):
		self.health -= 1
		if self.health < 0:
			# If enemy dies change the score, give the player an extra bullet and remove the enemy.
			self.game.enemies_killed += 1
			player.bullet_count += 1
			self.die()
			
	def bounceOfEdges(self):
		if self.shape.x + PLAYER_SIZE / 2 > MAP_SIZE:
			self.vx *= -1
		if self.shape.x - PLAYER_SIZE / 2 < -MAP_SIZE:
			self.vx *= -1
		if self.shape.y + PLAYER_SIZE / 2 > MAP_SIZE:
			self.vy *= -1
		if self.shape.y - PLAYER_SIZE / 2 < -MAP_SIZE:
			self.vy *= -1

	def die(self):
		# Remove self from games list of enemies then remove both shapes from the canvas.
		self.game.enemies.remove(self)
		self.game.canvas.remove(self.shape)
		self.game.canvas.remove(self.health_bar)