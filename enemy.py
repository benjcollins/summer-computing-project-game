from canvas import *
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

    def update(self, asteroids, player):
        self.moveEnemy(player)
        self.updateHealthBar()

    def updateHealthBar(self):
        self.health_bar.x = self.shape.x - PLAYER_SIZE / 2
        self.health_bar.y = self.shape.y - PLAYER_SIZE / 2
        self.health_bar.w = PLAYER_SIZE / self.max_health * self.health

    def moveEnemy(self, player):
        diffx = player.shape.x - self.shape.x
        diffy = player.shape.y - self.shape.y
        length = math.sqrt(diffx ** 2 + diffy ** 2)
        scale = self.speed / length
        self.shape.x += diffx * scale
        self.shape.y += diffy * scale

    def hit(self):
        self.health -= 1
        if self.health < 0:
            self.die()

    def die(self):
        self.game.enemies.remove(self)
        self.game.canvas.remove(self.shape)
        self.game.canvas.remove(self.health_bar)