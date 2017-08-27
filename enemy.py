#!/usr/bin/python3

from canvas.canvas import *
from consts import *
from bullet import *
from random import *
import math

class Enemy:

	def __init__(self, game, speed, health):
		self.game = game
		x = (random() * 2 - 1) * MAP_SIZE
		y = (random() * 2 - 1) * MAP_SIZE
		self.shape = Rect(x, y, PLAYER_SIZE, PLAYER_SIZE, DAMAGE_COLOR, layer = "content")
		right = x - PLAYER_SIZE / 2
		top = y - PLAYER_SIZE / 2
		self.health_bar = Rect(right, top, PLAYER_SIZE, PLAYER_SIZE, HEALTH_COLOR, layer = "content", flow = "right")
		self.game.canvas.add(self.shape)
		self.game.canvas.add(self.health_bar)
		self.speed = speed
		self.max_health = health
		self.health = health
		self.vx = 0
		self.vy = 0

	def update(self, asteroids, player):
		self.moveEnemy(player)
		self.bounceOfEdges()
		self.collideWithPlayer(player)
		self.shape.x += self.vx
		self.shape.y += self.vy
		self.updateHealthBar()
		
	def collideWithPlayer(self, player):
		xdist = abs(self.shape.x - player.shape.x)
		ydist = abs(self.shape.y - player.shape.y)
		xcheck = xdist < PLAYER_SIZE
		ycheck = ydist < PLAYER_SIZE
		
		if xcheck and ycheck:
			player.damage()
			self.die()

	def updateHealthBar(self):
		self.health_bar.x = self.shape.x - PLAYER_SIZE / 2
		self.health_bar.y = self.shape.y - PLAYER_SIZE / 2
		self.health_bar.w = PLAYER_SIZE / self.max_health * self.health

	def moveEnemy(self, player):
		diffx = player.shape.x - self.shape.x
		diffy = player.shape.y - self.shape.y
		length = math.sqrt(diffx ** 2 + diffy ** 2)
		scale = ENEMY_MAX_SPEED / length
		vx = diffx * scale
		vy = diffy * scale
		
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
		self.game.enemies.remove(self)
		self.game.canvas.remove(self.shape)
		self.game.canvas.remove(self.health_bar)