from canvas import *
from consts import *
from random import *
import time

class PowerUp:

	def __init__(self, game):
		self.game = game
		x = (random() * 2 - 1) * MAP_SIZE
		y = (random() * 2 - 1) * MAP_SIZE
		self.shape = Rect(x, y, POWERUP_SIZE, POWERUP_SIZE, POWERUP_COLORA, layer = "content")
		self.game.canvas.add(self.shape)
		self.color_change = time.time() + BLINK_DURATION
		self.text = False
		self.endpower = 0
		self.power = "none"
		self.next_shot = 0

	def update(self, player):
		if time.time() > self.color_change:
			self.color_change += BLINK_DURATION
			if self.shape.color == POWERUP_COLORA:
				self.shape.color = POWERUP_COLORB
				self.shape.w = POWERUP_SIZE
				self.shape.h = POWERUP_SIZE
				
				if self.text:
					self.text.font_size = 80
					self.text.color = POWERUP_COLORA
			else:
				self.shape.color = POWERUP_COLORA
				self.shape.w = POWERUP_BLINK_SIZE
				self.shape.h = POWERUP_BLINK_SIZE

				if self.text:
					self.text.font_size = 60
					self.text.color = POWERUP_COLORB

		if self.power != "none":
			if time.time() > self.endpower:
				self.game.canvas.remove(self.text)
				self.text = False
				self.power = "none"
				player.laserOff()

		if self.power == "rapid fire":
			if self.next_shot < time.time():
				self.next_shot += RAPID_FIRE_DURATION
				player.shoot(0, 0)

		hit = False
		for bullet in player.bullets:
			xcheck = abs(self.shape.x - bullet.shape.x) * 2 < BULLET_SIZE + POWERUP_BLINK_SIZE
			ycheck = abs(self.shape.y - bullet.shape.y) * 2 < BULLET_SIZE + POWERUP_BLINK_SIZE
			if xcheck and ycheck:
				hit = True
		
		if hit and self.power == "none":
			self.power = choice(["rapid fire", "laser"])
			self.text = Text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, self.power, POWERUP_COLORA, layer = "ui", font_size = 80, font_name = "FreeSans Bold")
			self.game.canvas.add(self.text)
			self.shape.x = (random() * 2 - 1) * MAP_SIZE
			self.shape.y = (random() * 2 - 1) * MAP_SIZE
			self.endpower = time.time() + POWERUP_DURATION

			if self.power == "rapid fire":
				self.next_shot = time.time() + RAPID_FIRE_DURATION

			if self.power == "laser":
				player.laserOn()