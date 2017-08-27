#!/usr/bin/python3

# Represents a bullet in the game.
# By BEN COLLINS

from canvas.canvas import *
from consts import *

class Bullet:

	def __init__(self, x, y, vx, vy, player):
		self.player = player
		self.vx = vx
		self.vy = vy

		# Create shape and add it to the canvas.
		self.shape = Rect(x, y, BULLET_SIZE, BULLET_SIZE, "#ffffff", layer = "content")
		self.player.game.canvas.add(self.shape)

		self.player.bullets.append(self)

	def update(self, asteroids, enemies):
		# Move bullet accroding to velocity.
		self.shape.x += self.vx
		self.shape.y += self.vy

		self.collideWithAsteroid(asteroids)
		self.collideWithEnemy(enemies)
		self.collideWithEdge()

	def collideWithAsteroid(self, asteroids):
		for a in asteroids:
			# Check if the distants between the object and asteroid is greater than there sizes.
			xdist = abs(self.shape.x - a.shape.x)
			ydist = abs(self.shape.y - a.shape.y)
			xcheck = xdist < a.size / 2
			ycheck = ydist < a.size / 2

			if xcheck and ycheck:
				# If hit bounce the bullet and tell the asteroid that it was hit.
				a.hit()
				if xdist > ydist:
					self.vx *= -1
				else:
					self.vy *= -1

	def collideWithEnemy(self, enemies):
		for e in enemies:
			# Check if the distants between the object and asteroid is greater than there sizes.
			xcheck = abs(self.shape.x - e.shape.x) < PLAYER_SIZE / 2
			ycheck = abs(self.shape.y - e.shape.y) < PLAYER_SIZE / 2

			if xcheck and ycheck:
				# If hit tell the enemy it was hit by player and remove bullet.
				e.hit(self.player)
				self.delete()

	def collideWithEdge(self):
		# If a bullet hits the edge it is removed to stop the screen from filling up.
		if self.shape.x > MAP_SIZE:
			self.delete()
		if self.shape.x < -MAP_SIZE:
			self.delete()
		if self.shape.y > MAP_SIZE:
			self.delete()
		if self.shape.y < -MAP_SIZE:
			self.delete()

	def delete(self):
		# Remove the bullet from the list of bullets in player and remove shape from canvas.
		# Try catch to prevent value errors caused by removing objects.
		try:
			self.player.bullets.remove(self)
			self.player.game.canvas.remove(self.shape)
		except ValueError:
			pass