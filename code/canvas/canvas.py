#!/usr/bin/python3

# A wrapper around pygame that gives you an object based drawing system and asynchronous callbacks.
# By BEN COLLINS

import pygame
from threading import *
from canvas.rect import *
from canvas.text import *
from canvas.polygon import *

pygame.init()

class Canvas (Thread):
	
	def __init__(self, width, height, title, layers = ["default"]):
		# The canvas runs in its own thread to improve performance and so it draws as many times as possbile.
		Thread.__init__(self)
		
		self.width = width
		self.height = height
		self.running = True
		self.color = "#ffffff"
		self.keys = {}

		# Set all callbacks to false or empty to begin with.
		self.on_mouse_down = False
		self.on_mouse_up = False
		self.mouse_down = False
		self.key_down_callbacks = {}
		self.key_up_callbacks = {}

		# Create the layer data from the users input.
		self.layerNames = layers
		self.layerOffsets = []
		self.layers = []
		for i in layers:
			self.layers.append([])
			self.layerOffsets.append((0, 0))
		
		# Create the pygame window with the given size and set the title.
		self.window = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption(title)
		
	def run(self):
		
		while self.running:
			# Get pygame events and if necessary hand them onto the user via a callback.
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
					try:
						self.keys.pop(key)
					except KeyError:
						pass
					if key in self.key_up_callbacks:
						self.key_up_callbacks[key]()
			
			# Convert the hex value of background color into an (r, g, b) tuple.
			r = int(self.color[1:3], 16)
			g = int(self.color[3:5], 16)
			b = int(self.color[5:7], 16)
			color = (r, g, b)
			self.window.fill(color)
			
			# Clear the screen and draw all shapes in the order of there layers.
			for layer in self.layers:
				for shape in layer:
					shape.draw(self)
			
			pygame.display.flip()

		# When the window is no longer 'running' kill the window.
		pygame.display.quit()
		
	def add(self, shape):
		# Find the shapes layer and it to that layers list.
		for i in range(0, len(self.layerNames)):
			name = self.layerNames[i]
			if name == shape.layer:
				self.layers[i].append(shape)

	def setLayerOffset(self, x, y, layer):
		# Allow the user to set offsets for the individual layers.
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
		
	# Setters the the callbacks.
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
				try:
					self.layers[i].remove(shape)
				except ValueError:
					pass