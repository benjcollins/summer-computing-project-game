from canvas.canvas import *
from consts import *
from bullet import *
import math
import random

class Player:

	def __init__(self, game):
		self.game = game
		self.game.canvas.set_on_mouse_down(self.shoot)
		self.crosshair1 = Polygon([(0, 0), (0, 0)], "#ffffff", thickness = 3, layer = "content")
		self.crosshair2 = Polygon([(0, 0), (0, 0)], "#ffffff", thickness = 3, layer = "content")
		self.shape = Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE, PLAYER_COLOR, layer = "content")
		self.direction = "none"
		self.vx = 0
		self.vy = 0
		self.accuracy = 0
		self.bullets = []
		self.health_green = Rect(0, 0, WINDOW_WIDTH, 20, HEALTH_COLOR, layer = "ui", flow = "right")
		self.health_red = Rect(0, 0, WINDOW_WIDTH, 20, DAMAGE_COLOR, layer = "ui", flow = "right")
		self.alive = True
		self.bullet_count = 1

		self.game.canvas.add(self.crosshair1)
		self.game.canvas.add(self.crosshair2)
		self.game.canvas.add(self.shape)
		self.game.canvas.add(self.health_red)
		self.game.canvas.add(self.health_green)

	def update(self, asteroids, enemies):
		self.bounceOfEdges()
		self.drawCrossHair()
		self.updateBullets(asteroids, enemies)
		self.shape.x += self.vx
		self.shape.y += self.vy

	def bounceOfEdges(self):
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

		cross1x = self.shape.x + math.cos(max_) * CROSSHAIR_SIZE
		cross1y = self.shape.y + math.sin(max_) * CROSSHAIR_SIZE
		cross2x = self.shape.x + math.cos(min_) * CROSSHAIR_SIZE
		cross2y = self.shape.y + math.sin(min_) * CROSSHAIR_SIZE
		
		self.crosshair1.points[0] = (self.shape.x, self.shape.y)
		self.crosshair2.points[0] = (self.shape.x, self.shape.y)
		self.crosshair1.points[1] = (cross1x, cross1y)
		self.crosshair2.points[1] = (cross2x, cross2y)

		if self.accuracy > 0:
			self.accuracy -= COOLDOWN_FACTOR

	def updateBullets(self, asteroids, enemies):
		for bullet in self.bullets:
			bullet.update(asteroids, enemies)

	def shoot(self, x, y):
		min_, max_ = self.calcMaxAndMin()
		self.bullet_count = max(self.bullet_count, 1)
		self.bullet_count = min(self.bullet_count, MAX_BULLETS)
		recoilx = 0
		recoily = 0

		for i in range(0, self.bullet_count):
			direction = min_ + random.random() * (max_ - min_)
			vx = math.cos(direction) * BULLET_SPEED
			vy = math.sin(direction) * BULLET_SPEED
			b = Bullet(self.shape.x, self.shape.y, vx, vy, self)
			recoilx += b.vx
			recoily += b.vy
			
		self.vx -= recoilx / self.bullet_count * RECOIL_FACTOR
		self.vy -= recoily / self.bullet_count * RECOIL_FACTOR

		self.accuracy += 5
		self.accuracy = min(self.accuracy, 60)

	def calcMaxAndMin(self):
		mx = self.game.canvas.mouse_x - self.game.canvas.getLayerOffsetX("content") - self.shape.x
		my = self.game.canvas.mouse_y - self.game.canvas.getLayerOffsetY("content") - self.shape.y

		if mx == 0:
			mx = 0.0001
		if my == 0:
			my = 0.0001

		theta = math.atan(my / mx)
		if mx < 0:
			theta = theta - math.pi

		max_ = theta - math.radians(self.accuracy)
		min_ = theta + math.radians(self.accuracy)

		return (min_, max_)
		
	def damage(self):
		self.health_green.w -= WINDOW_WIDTH / MAX_HEALTH
		self.bullet_count = 0
		if not self.health_green.w > 0:
			self.alive = False