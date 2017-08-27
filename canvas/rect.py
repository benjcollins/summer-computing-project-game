#!/usr/bin/python3

import pygame

pygame.init()

class Rect:
	
	def __init__(self, x, y, w, h, color, thickness = 0, flow = "center", layer = "default"):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.color = color
		self.flow = flow
		self.thickness = thickness
		self.layer = layer
		
	def draw(self, canvas):
		# Work out the users flow and ajust the x and y accordingly.
		# Also add the layer offsets and this point.
		if self.flow == "center":
			x = self.x - self.w / 2 + canvas.getLayerOffsetX(self.layer)
			y = self.y - self.h / 2 + canvas.getLayerOffsetY(self.layer)
		
		if self.flow == "right":
			x = self.x + canvas.getLayerOffsetX(self.layer)
			y = self.y + canvas.getLayerOffsetY(self.layer)
			
		if self.flow == "left":
			x = self.x - self.w + canvas.getLayerOffsetX(self.layer)
			y = self.y - self.h + canvas.getLayerOffsetY(self.layer)
		
		coords = (x, y, self.w, self.h)
			
		# Convert hex color to (r, g, b) tuple.
		r = int(self.color[1:3], 16)
		g = int(self.color[3:5], 16)
		b = int(self.color[5:7], 16)
		color = (r, g, b)
		
		# If the shape is inside the screen draw it.
		if x < canvas.width and x + self.w > 0:
		    if y < canvas.height and y + self.h > 0:
		        pygame.draw.rect(canvas.window, color, coords, self.thickness)