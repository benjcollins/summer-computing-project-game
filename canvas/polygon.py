#!/usr/bin/python3

import pygame

pygame.init()

class Polygon:

    def __init__(self, points, color, closed = False, fill = False, thickness = 2, layer = "default"):
        self.points = points
        self.color = color
        self.closed = closed
        self.fill = fill
        self.thickness = thickness
        self.layer = layer

    def draw(self, canvas):

        r = int(self.color[1:3], 16)
        g = int(self.color[3:5], 16)
        b = int(self.color[5:7], 16)
        color = (r, g, b)
        
        points = []
        for point in self.points:
            x = point[0] + canvas.getLayerOffsetX(self.layer)
            y = point[1] + canvas.getLayerOffsetY(self.layer)
            points.append((x, y))
        
        if len(points) == 2:
            pygame.draw.line(canvas.window, color, points[0], points[1], self.thickness)
            
        if self.fill:
            pygame.draw.polygon(canvas.window, color, points, 0)
        else:
            if self.closed:
                pygame.draw.lines(canvas.window, color, True, points, self.thickness)
                # or pygame.draw.polygon(canvas.window, color, points, self.thickness)
            else:
                pygame.draw.lines(canvas.window, color, False, points, self.thickness)