import pygame

pygame.init()
pygame.font.init()

class Text:

	def __init__(self, x, y, text, color, font_name = "monospace", font_size = 15, layer = "default", flow = "center"):
		self.x = x
		self.y = y
		self.text = text
		self.old_text = text
		self.color = color
		self.old_color = color
		self.font_name = font_name
		self.old_font_name = font_name
		self.font_size = font_size
		self.old_font_size = font_size
		self.layer = layer
		self.flow = flow

		r = int(self.color[1:3], 16)
		g = int(self.color[3:5], 16)
		b = int(self.color[5:7], 16)
		color = (r, g, b)
		self.font = pygame.font.SysFont(self.font_name, self.font_size)
		self.w, self.h = self.font.size(self.text)
		self.label = self.font.render(self.text, 1, color)

	def draw(self, canvas):

		name_change = self.font_name != self.old_font_name
		size_change = self.font_size != self.old_font_size

		if name_change or size_change:
			self.font = pygame.font.SysFont(self.font_name, self.font_size)
			self.old_font_name = self.font_name
			self.old_font_size = self.font_size

		text_change = self.text != self.old_text
		color_change = self.color != self.old_color

		if text_change or color_change or name_change or size_change:

			r = int(self.color[1:3], 16)
			g = int(self.color[3:5], 16)
			b = int(self.color[5:7], 16)
			color = (r, g, b)

			self.w, self.h = self.font.size(self.text)
			self.label = self.font.render(self.text, 1, color)
			self.old_text = self.text
			self.old_color = self.old_color

		if self.flow == "center":
			x = self.x - self.w / 2 + canvas.getLayerOffsetX(self.layer)
			y = self.y - self.h / 2 + canvas.getLayerOffsetY(self.layer)
		
		if self.flow == "right":
			x = self.x + canvas.getLayerOffsetX(self.layer)
			y = self.y + canvas.canvas.getLayerOffsetY(self.layer)
			
		if self.flow == "left":
			x = self.x - self.w + canvas.getLayerOffsetX(self.layer)
			y = self.y - self.h + canvas.getLayerOffsetY(self.layer)
			
		canvas.window.blit(self.label, (x, y))