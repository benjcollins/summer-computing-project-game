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
		self.canvas = Canvas(WINDOW_WIDTH, WINDOW_HEIGHT, "Game", ["background", "content", "ui"])
		self.canvas.color = "#05050a"
		self.nextFrame = time.clock()
		self.canvas.setLayerOffset(300, 200, "content")
		self.enemies = []
		self.enemy_count = 1
		self.enemy_health = ENEMY_START_HEALTH
		self.enemy_speed = ENEMY_START_SPEED
		self.enemies_killed = 0
		self.score = Text(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50, "Score: 0", "#ffffff", layer = "ui", font_size = 35, font_name = "FreeSans Bold")
		
		for i in range(0, 100):
			x = (random() * 2 - 1) * MAP_SIZE
			y = (random() * 2 - 1) * MAP_SIZE
			self.canvas.add(Rect(x, y, 1, 1, "#ffffff", layer = "background"))
		for i in range(0, 100):
			x = (random() * 2 - 1) * MAP_SIZE
			y = (random() * 2 - 1) * MAP_SIZE
			self.canvas.add(Rect(x, y, 3, 3, "#ffffff", layer = "content"))
			
		self.asteroids = []
		for i in range(0, 15):
			asteroid = Asteroid(self)
			self.asteroids.append(asteroid)

		self.canvas.add(Polygon([(-MAP_SIZE, -MAP_SIZE), (MAP_SIZE, -MAP_SIZE)], "#ffffff", thickness = 3, layer = "content"))
		self.canvas.add(Polygon([(MAP_SIZE, -MAP_SIZE), (MAP_SIZE, MAP_SIZE)], "#ffffff", thickness = 3, layer = "content"))
		self.canvas.add(Polygon([(MAP_SIZE, MAP_SIZE), (-MAP_SIZE, MAP_SIZE)], "#ffffff", thickness = 3, layer = "content"))
		self.canvas.add(Polygon([(-MAP_SIZE, MAP_SIZE), (-MAP_SIZE, -MAP_SIZE)], "#ffffff", thickness = 3, layer = "content"))
		self.canvas.add(self.score)

		self.powerup = PowerUp(self)
		self.player = Player(self)

		self.canvas.start()
		self.loop()

	def loop(self):
		while self.canvas.running and self.player.alive:
			if self.nextFrame < time.clock():
				self.nextFrame += TIME_STEP
				self.update()
				
		if self.canvas.running:
			msg = Text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, "GAME OVER", "#ff0000", layer = "ui", font_size = 80, font_name = "FreeSans Bold")
			
			self.canvas.add(msg)
			time.sleep(2)
			self.canvas.remove(msg)
			time.sleep(1)
			
			msg.text = "Enemies Killed: " + str(self.enemies_killed)
			self.canvas.add(msg)
			time.sleep(2)
			self.canvas.remove(msg)
			time.sleep(1)
			
			msg.text = "Better luck next time!"
			self.canvas.add(msg)
			time.sleep(3)
			
			self.canvas.running = False

	def update(self):
		
		offsetx = self.canvas.getLayerOffsetX("content")
		offsety = self.canvas.getLayerOffsetY("content")
		offsetxchange = offsetx
		offsetychange = offsety

		if self.player.shape.x + offsetx > WINDOW_WIDTH * 0.7:
			offsetxchange -= self.player.shape.x + offsetx - WINDOW_WIDTH * 0.7
		if self.player.shape.x + offsetx < WINDOW_WIDTH * 0.3:
			offsetxchange -= self.player.shape.x + offsetx - WINDOW_WIDTH * 0.3
		if self.player.shape.y + offsety > WINDOW_HEIGHT * 0.7:
			offsetychange -= self.player.shape.y + offsety - WINDOW_HEIGHT * 0.7
		if self.player.shape.y + offsety < WINDOW_HEIGHT * 0.3:
			offsetychange -= self.player.shape.y + offsety - WINDOW_HEIGHT * 0.3

		self.canvas.setLayerOffset(offsetxchange, offsetychange, "content")
		
		for asteroid in self.asteroids:
			asteroid.update(self.player, self.enemies)

		for enemy in self.enemies:
			enemy.update(self.asteroids, self.player)

		self.powerup.update(self.player)
		self.player.update(self.asteroids, self.enemies)

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