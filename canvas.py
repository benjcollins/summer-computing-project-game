import pygame
from threading import *
from rect import *
from text import *
from polygon import *

pygame.init()

class Canvas (Thread):
	
	def __init__(self, width, height, title, layers = ["default"]):
		Thread.__init__(self)
		
		self.width = width
		self.height = height

		self.layerNames = layers
		self.layerOffsets = []
		self.layers = []
		for i in layers:
			self.layers.append([])
			self.layerOffsets.append((0, 0))

		self.running = True
		self.color = "#ffffff"
		self.keys = {}

		self.on_mouse_down = False
		self.on_mouse_up = False
		self.mouse_down = False

		self.key_down_callbacks = {}
		self.key_up_callbacks = {}
		
		self.window = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption(title)
		
	def run(self):
		
		while self.running:
			events = pygame.event.get()
			for event in events:
				
				x, y = pygame.mouse.get_pos()
				self.mouse_x = x
				self.mouse_y = y
				
				button = False
				buttons = pygame.mouse.get_pressed()
				for button in buttons:
					if button:
						self.button = True
						break
				
				if event.type == pygame.QUIT:
					self.running = False
					
				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.on_mouse_down:
						self.on_mouse_down(x, y)
				
				if event.type == pygame.MOUSEBUTTONUP:
					if self.on_mouse_up:
						self.on_mouse_up(x, y)
						
				if event.type == pygame.KEYDOWN:
					key = pygame.key.name(event.key)
					self.keys[key] = True
					if key in self.key_down_callbacks:
						self.key_down_callbacks[key]()
				
				if event.type == pygame.KEYUP:
					key = pygame.key.name(event.key)
					self.keys.pop(key)
					if key in self.key_up_callbacks:
						self.key_up_callbacks[key]()
				
			r = int(self.color[1:3], 16)
			g = int(self.color[3:5], 16)
			b = int(self.color[5:7], 16)
			color = (r, g, b)
			self.window.fill(color)
			
			for layer in self.layers:
				for shape in layer:
					shape.draw(self)
			
			pygame.display.flip()
		
	def add(self, shape):
		for i in range(0, len(self.layerNames)):
			name = self.layerNames[i]
			if name == shape.layer:
				self.layers[i].append(shape)

	def setLayerOffset(self, x, y, layer):
		for i in range(0, len(self.layerNames)):
			name = self.layerNames[i]
			if name == layer:
				self.layerOffsets[i] = (x, y)

	def getLayerOffsetX(self, layer):
		for i in range(0, len(self.layerNames)):
			name = self.layerNames[i]
			if name == layer:
				return self.layerOffsets[i][0]

	def getLayerOffsetY(self, layer):
		for i in range(0, len(self.layerNames)):
			name = self.layerNames[i]
			if name == layer:
				return self.layerOffsets[i][1]
		
	def set_on_mouse_down(self, callback):
		self.on_mouse_down = callback
		
	def set_on_mouse_up(self, callback):
		self.on_mouse_up = callback
		
	def on_key_down(self, key, callback):
		self.key_down_callbacks[key] = callback
		
	def on_key_up(self, key, callback):
		self.key_up_callbacks[key] = callback
		
	def getKey(self, key):
		if key in self.keys:
			return self.keys[key]
		else:
			return False

	def remove(self, shape):
		for i in range(0, len(self.layerNames)):
			name = self.layerNames[i]
			if name == shape.layer:
				self.layers[i].remove(shape)