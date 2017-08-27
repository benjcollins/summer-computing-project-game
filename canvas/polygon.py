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

        # Convert hex color to (r, g, b) tuple.
        r = int(self.color[1:3], 16)
        g = int(self.color[3:5], 16)
        b = int(self.color[5:7], 16)
        color = (r, g, b)
        
        # Move all points according to that layers offset.
        points = []
        for point in self.points:
            x = point[0] + canvas.getLayerOffsetX(self.layer)
            y = point[1] + canvas.getLayerOffsetY(self.layer)
            points.append((x, y))
        
        if len(points) == 2:
            # If the number of points is 2 draw a line instead.
            pygame.draw.line(canvas.window, color, points[0], points[1], self.thickness)

        elif self.fill:
            # If the shape is filled draw a polygon.
            pygame.draw.polygon(canvas.window, color, points, 0)
        else:
            if self.closed:
                # If the shape is closed of draw either an array of lines or a polygon.
                pygame.draw.lines(canvas.window, color, True, points, self.thickness)
                # or pygame.draw.polygon(canvas.window, color, points, self.thickness)
            else:
                # If the shape is not closed draw an array of lines.
                pygame.draw.lines(canvas.window, color, False, points, self.thickness)