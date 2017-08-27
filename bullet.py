from canvas.canvas import *
from consts import *

class Bullet:

	def __init__(self, x, y, vx, vy, player):
		self.shape = Rect(x, y, BULLET_SIZE, BULLET_SIZE, "#ffffff", layer = "content")
		self.player = player
		player.game.canvas.add(self.shape)
		player.bullets.append(self)
		self.vx = vx
		self.vy = vy

	def update(self, asteroids, enemies):
		self.shape.x += self.vx
		self.shape.y += self.vy

		for a in asteroids:
			xdist = abs(self.shape.x - a.shape.x)
			ydist = abs(self.shape.y - a.shape.y)
			xcheck = xdist < a.size / 2
			ycheck = ydist < a.size / 2
			if xcheck and ycheck:
				a.hit()
				if xdist > ydist:
					self.vx *= -1
				else:
					self.vy *= -1

		for e in enemies:
			xcheck = abs(self.shape.x - e.shape.x) < PLAYER_SIZE / 2
			ycheck = abs(self.shape.y - e.shape.y) < PLAYER_SIZE / 2
			if xcheck and ycheck:
				e.hit(self.player)
				self.delete()

		if self.shape.x > MAP_SIZE:
			self.delete()
		if self.shape.x < -MAP_SIZE:
			self.delete()
		if self.shape.y > MAP_SIZE:
			self.delete()
		if self.shape.y < -MAP_SIZE:
			self.delete()

	def delete(self):
		try:
			self.player.bullets.remove(self)
			self.player.game.canvas.remove(self.shape)
		except ValueError:
			pass