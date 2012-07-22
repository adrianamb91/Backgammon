import pyglet
from pyglet.gl import *
from pyglet.graphics import *
import math

class Gradient(object):
    def __init__(self, start_color, end_color):
        self.start_color = start_color
        self.end_color = end_color
        self.gradient_parts = []
        self.levels = 0


    def render(self):
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        for part in self.gradient_parts[:self.levels]:
            part.draw(pyglet.gl.GL_LINE_LOOP)
        pyglet.gl.glDisable(pyglet.gl.GL_BLEND)


class CircularGradient(Gradient):
    points = 60
    angle_step = math.pi * 2 / points

    def __init__(self, x, y, start_color, end_color, start_radius, end_radius):
        Gradient.__init__(self, start_color, end_color)
        self.draw(x, y, start_radius, end_radius)


    def draw(self, x, y, start_radius, end_radius):
        delta_radius = end_radius - start_radius
        levels = int(abs(delta_radius) + 1)
        overflow = int(abs(delta_radius) * 0.3)
        self.levels = levels + overflow

        if levels > 1:
            radius_step = delta_radius / abs(delta_radius)

            red_step = (self.end_color[0] - self.start_color[0]) / levels
            green_step = (self.end_color[1] - self.start_color[1]) / levels
            blue_step = (self.end_color[2] - self.start_color[2]) / levels
            alpha_step = (self.end_color[3] - self.start_color[3]) / levels

            vertex_array = []
            color_array = []

            for i in range(levels + overflow):
                if i <= levels: factor = i
                else: factor = levels

                radius = start_radius + factor * radius_step
                color = [self.start_color[0] + red_step * factor,
                         self.start_color[1] + green_step * factor,
                         self.start_color[2] + blue_step * factor,
                         self.start_color[3] + alpha_step * factor]

                vertex_array = []
                color_array = []

                for j in range(self.points):
                    w = radius * math.cos(self.angle_step * j)
                    h = radius * math.sin(self.angle_step * j)

                    vertex_array.append(x + w)
                    vertex_array.append(y + h)
                    for c in color:
                        color_array.append(c)

                if i >= len(self.gradient_parts):
                    self.gradient_parts.append(
                        pyglet.graphics.vertex_list(self.points,
                                                    ('v2f', vertex_array),
                                                    ('c4f', color_array)))
                else:
                    self.gradient_parts[i].vertices = vertex_array
                    self.gradient_parts[i].colors = color_array


class RectGradient(Gradient):
    def __init__(self, x, y, width, height, start_color, end_color, start_radius, end_radius):
        Gradient.__init__(self, start_color, end_color)
        self.draw(x, y, width, height, start_radius, end_radius)


    def draw(self, x, y, width, height, start_radius, end_radius):
        delta_radius = end_radius - start_radius
        levels = int(abs(delta_radius) + 1)
        self.levels = levels

        if levels > 1:
            radius_step = delta_radius / abs(delta_radius)

            red_step = (self.end_color[0] - self.start_color[0]) / levels
            green_step = (self.end_color[1] - self.start_color[1]) / levels
            blue_step = (self.end_color[2] - self.start_color[2]) / levels
            alpha_step = (self.end_color[3] - self.start_color[3]) / levels

            big_offset = [(0, 0), (1, 0), (1, 1), (0, 1)]
            small_offset = [(1, 1), (-1, 1), (-1, -1), (1, -1)]

            for i in range(levels):
                radius = start_radius + i * radius_step
                color = [self.start_color[0] + red_step * i,
                         self.start_color[1] + green_step * i,
                         self.start_color[2] + blue_step * i,
                         self.start_color[3] + alpha_step * i]

                vertex_array = []
                color_array = []

                for j in range(4):
                    vertex_array.append(x + width * big_offset[j][0] + radius * small_offset[j][0])
                    vertex_array.append(y + height * big_offset[j][1] + radius * small_offset[j][1])
                    for c in color:
                        if c < 0: c = 0
                        elif c > 1: c = 1
                        color_array.append(c)

                if i >= len(self.gradient_parts):
                    self.gradient_parts.append(
                        pyglet.graphics.vertex_list(4,
                                                    ('v2f', vertex_array),
                                                    ('c4f', color_array)))
                else:
                    self.gradient_parts[i].vertices = vertex_array
                    self.gradient_parts[i].colors = color_array


if __name__ == '__main__':
    "Please do not run this file directly, include it."
