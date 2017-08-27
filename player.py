#!/usr/bin/python3

# Represents the player for the game.
# By BEN COLLINS

from canvas.canvas import *
from consts import *
from bullet import *
import math
import random

class Player:

	def __init__(self, game):
		self.game = game
		self.direction = "none"
		self.vx = 0
		self.vy = 0
		self.accuracy = 0
		self.bullets = []
		self.alive = True
		self.bullet_count = 1

		# Use the canvas to create a mouse binding to the shoot method.
		self.game.canvas.set_on_mouse_down(self.shoot)

		# Create the crosshair shapes and add them to the canvas.
		self.crosshair1 = Polygon([(0, 0), (0, 0)], "#ffffff", thickness = 3, layer = "content")
		self.game.canvas.add(self.crosshair1)
		self.crosshair2 = Polygon([(0, 0), (0, 0)], "#ffffff", thickness = 3, layer = "content")
		self.game.canvas.add(self.crosshair2)

		# Create the players main shape and add it to the canvas.
		self.shape = Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE, PLAYER_COLOR, layer = "content")
		self.game.canvas.add(self.shape)
		
		# Create shapes for the players health bar and add them to the canvas.
		self.health_red = Rect(0, WINDOW_HEIGHT - 20, WINDOW_WIDTH, 20, DAMAGE_COLOR, layer = "ui", flow = "right")
		self.game.canvas.add(self.health_red)
		self.health_yellow = Rect(0, WINDOW_HEIGHT - 20, WINDOW_WIDTH, 20, RESTORE_COLOR, layer = "ui", flow = "right")
		self.game.canvas.add(self.health_yellow)
		self.health_green = Rect(0, WINDOW_HEIGHT - 20, WINDOW_WIDTH, 20, HEALTH_COLOR, layer = "ui", flow = "right")
		self.game.canvas.add(self.health_green)

	def update(self, asteroids, enemies):
		self.bounceOfEdges()
		self.drawCrossHair()
		self.updateBullets(asteroids, enemies)
		self.updateRestore()

		# Move players shape by its velocity.
		self.shape.x += self.vx
		self.shape.y += self.vy

	def updateRestore(self):
		# If player is hit and the green bar is less than the yellow bar the yellow bar slowly moves downwards
		# at a rate that is proportional to the difference between the two bars.
		if self.health_yellow.w > self.health_green.w:
			diff = self.health_yellow.w - self.health_green.w
			self.health_yellow.w -= diff / RESTORE_SPEED

	def bounceOfEdges(self):
		# If the player moves over the edges bounce off in the correct axis.
		if self.shape.x + PLAYER_SIZE / 2 > MAP_SIZE:
			self.vx *= -1
		if self.shape.x - PLAYER_SIZE / 2 < -MAP_SIZE:
			self.vx *= -1
		if self.shape.y + PLAYER_SIZE / 2 > MAP_SIZE:
			self.vy *= -1
		if self.shape.y - PLAYER_SIZE / 2 < -MAP_SIZE:
			self.vy *= -1

	def drawCrossHair(self):
		min_, max_ = self.calcMaxAndMin()

		# Calculate the position of the crossahirs using the min and max values of the players range.
		cross1x = self.shape.x + math.cos(max_) * CROSSHAIR_SIZE
		cross1y = self.shape.y + math.sin(max_) * CROSSHAIR_SIZE
		cross2x = self.shape.x + math.cos(min_) * CROSSHAIR_SIZE
		cross2y = self.shape.y + math.sin(min_) * CROSSHAIR_SIZE
		
		# Set the crosshairs position.
		self.crosshair1.points[0] = (self.shape.x, self.shape.y)
		self.crosshair2.points[0] = (self.shape.x, self.shape.y)
		self.crosshair1.points[1] = (cross1x, cross1y)
		self.crosshair2.points[1] = (cross2x, cross2y)

		# Apply a cooldown factor to the players accuracy.
		if self.accuracy > 0:
			self.accuracy -= COOLDOWN_FACTOR

	def updateBullets(self, asteroids, enemies):
		for bullet in self.bullets:
			bullet.update(asteroids, enemies)

	def shoot(self, x, y):

		# Set the maximum and minimum value of the number of bullets before the player shoots.
		self.bullet_count = max(self.bullet_count, 1)
		self.bullet_count = min(self.bullet_count, MAX_BULLETS)

		min_, max_ = self.calcMaxAndMin()
		recoilx = 0
		recoily = 0

		for i in range(0, self.bullet_count):
			# Calculate a random angle between the players crosshairs.
			direction = min_ + random.random() * (max_ - min_)
			# Use trig to convert this into a vector.
			vx = math.cos(direction) * BULLET_SPEED
			vy = math.sin(direction) * BULLET_SPEED
			# Create a bullet object with that velocity.
			b = Bullet(self.shape.x, self.shape.y, vx, vy, self)
			# Add the recoil of the bullet to the count.
			recoilx += b.vx
			recoily += b.vy

		# Get the average of all the recoil values and multiply by the recoil factor.	
		self.vx -= recoilx / self.bullet_count * RECOIL_FACTOR
		self.vy -= recoily / self.bullet_count * RECOIL_FACTOR

		# Decrease the players accuracy each time they shoot.
		self.accuracy += 5
		self.accuracy = min(self.accuracy, 60)

	def calcMaxAndMin(self):
		# Get the x and y of the mouse and make it relative to the players position.
		mx = self.game.canvas.mouse_x - self.game.canvas.getLayerOffsetX("content") - self.shape.x
		my = self.game.canvas.mouse_y - self.game.canvas.getLayerOffsetY("content") - self.shape.y

		# Make sure the values are not 0 because this will give a divide by 0 error.
		if mx == 0:
			mx = 0.0001
		if my == 0:
			my = 0.0001

		# Caclulate the angle the mouse it pointing at.
		theta = math.atan(my / mx)
		# Make it wrap round properly.
		if mx < 0:
			theta = theta - math.pi

		# Calculate the max and minimum angles of the players accuracy.
		max_ = theta - math.radians(self.accuracy)
		min_ = theta + math.radians(self.accuracy)

		return (min_, max_)
		
	def damage(self):
		# Decrease health by 1
		self.health_green.w -= WINDOW_WIDTH / MAX_HEALTH
		# Reset the number of bullets.
		self.bullet_count = 1
		if not self.health_green.w > 0:
			# If the health is zero the player is no longer 'alive'.
			self.alive = False