#!/usr/bin/python3

from networking import *
from canvas.canvas import *
from player import *
from asteroid import *
from consts import *
from random import *
from enemy import *
from powerup import *
import time

class Game:

	def __init__(self):
		# Create canvas object and set various its properties.
		self.canvas = Canvas(WINDOW_WIDTH, WINDOW_HEIGHT, "Game", ["background", "content", "ui"])
		self.canvas.setLayerOffset(300, 200, "content")
		self.canvas.color = "#05050a"

		# Setup array to hold enemies and counters for health speed and number at a time.
		self.enemies = []
		self.enemy_count = 1
		self.enemy_health = ENEMY_START_HEALTH
		self.enemy_speed = ENEMY_START_SPEED
		self.enemies_killed = 0

		# The next frame the update function will be called.
		self.nextFrame = time.clock()

		# Create score text and add it to the canvas.
		x = WINDOW_WIDTH / 2
		y = WINDOW_HEIGHT - 50
		self.score = Text(x, y, "", "#ffffff", layer = "ui", font_size = 35, font_name = "FreeSans Bold")
		self.canvas.add(self.score)
		
		# Add stars the to the canvas that do not move with the camera and are smaller (background stars).
		for i in range(0, 100):
			x = (random() * 2 - 1) * MAP_SIZE
			y = (random() * 2 - 1) * MAP_SIZE
			self.canvas.add(Rect(x, y, 1, 1, "#ffffff", layer = "background"))

		# Add stars the to the canvas that do move with the camera and are larger (foreground stars).
		for i in range(0, 100):
			x = (random() * 2 - 1) * MAP_SIZE
			y = (random() * 2 - 1) * MAP_SIZE
			self.canvas.add(Rect(x, y, 3, 3, "#ffffff", layer = "content"))
			
		self.asteroids = []
		for i in range(0, ASTEROID_COUNT):
			asteroid = Asteroid(self)
			self.asteroids.append(asteroid)

		# Add the four outer walls to the canvas.
		points = [(-MAP_SIZE, -MAP_SIZE), (MAP_SIZE, -MAP_SIZE)]
		self.canvas.add(Polygon(points, "#ffffff", thickness = 3, layer = "content"))
		points = [(MAP_SIZE, -MAP_SIZE), (MAP_SIZE, MAP_SIZE)]
		self.canvas.add(Polygon(points, "#ffffff", thickness = 3, layer = "content"))
		points = [(MAP_SIZE, MAP_SIZE), (-MAP_SIZE, MAP_SIZE)]
		self.canvas.add(Polygon(points, "#ffffff", thickness = 3, layer = "content"))
		points = [(-MAP_SIZE, MAP_SIZE), (-MAP_SIZE, -MAP_SIZE)]
		self.canvas.add(Polygon(points, "#ffffff", thickness = 3, layer = "content"))

		self.powerup = PowerUp(self)
		self.player = Player(self)

		# Start the canvas thread.
		self.canvas.start()
		self.loop()

	def loop(self):
		while self.canvas.running and self.player.alive:
			if self.nextFrame < time.clock():
				# If its time to compute the next frame do so and reset the next frame variable.
				self.nextFrame += TIME_STEP
				self.update()

		# Display the 'game over' message.
		x = WINDOW_WIDTH / 2
		y = WINDOW_HEIGHT / 2
		txt = "Game Over"
		msg = Text(x, y, txt, DAMAGE_COLOR, layer = "ui", font_size = 80, font_name = "FreeSans Bold")
		self.canvas.add(msg)

	def update(self):
		
		# Get the current layer offset (camera).
		offsetx = self.canvas.getLayerOffsetX("content")
		offsety = self.canvas.getLayerOffsetY("content")
		offsetxchange = offsetx
		offsetychange = offsety

		# If the player moves over a certain threshold the camera is updated so the player is always inside the view.
		if self.player.shape.x + offsetx > WINDOW_WIDTH * 0.6:
			offsetxchange -= self.player.shape.x + offsetx - WINDOW_WIDTH * 0.6
		if self.player.shape.x + offsetx < WINDOW_WIDTH * 0.4:
			offsetxchange -= self.player.shape.x + offsetx - WINDOW_WIDTH * 0.4
		if self.player.shape.y + offsety > WINDOW_HEIGHT * 0.6:
			offsetychange -= self.player.shape.y + offsety - WINDOW_HEIGHT * 0.6
		if self.player.shape.y + offsety < WINDOW_HEIGHT * 0.4:
			offsetychange -= self.player.shape.y + offsety - WINDOW_HEIGHT * 0.4

		# Apply this change to the canvas.
		self.canvas.setLayerOffset(offsetxchange, offsetychange, "content")
		
		for asteroid in self.asteroids:
			asteroid.update(self.player, self.enemies)

		for enemy in self.enemies:
			enemy.update(self.asteroids, self.player)

		self.powerup.update(self.player)
		self.player.update(self.asteroids, self.enemies)

		# If there are no enemies left send in the next wave which should be more powerful than the last.
		if len(self.enemies) == 0:
			if self.enemy_count >= MAX_ENEMIES:
				self.enemy_count = 1
				self.enemy_health += 1
			if self.enemy_health >= ENEMY_MAX_HEALTH:
				self.enemy_health = ENEMY_START_HEALTH
				self.enemy_speed += ENEMY_SPEED_INCREASE

			self.enemy_count += 1

			for i in range(0, self.enemy_count):
				self.enemies.append(Enemy(self, self.enemy_speed, self.enemy_health))
				
		self.score.text = "Enemies Killed: " + str(self.enemies_killed)

Game()