import pyglet
from pyglet.gl import *
from pyglet.graphics import *
import math


class Outline(object):
    primitive_parts = None
    coord_nr = {}

    def __init__(self, vertices, color):
        self.draw(vertices, color)

    def render(self, style = pyglet.gl.GL_LINE_LOOP):
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        for part in self.primitive_parts[:self.levels]:
            part.draw(style)
        pyglet.gl.glDisable(pyglet.gl.GL_BLEND)

    def draw(self, vertices_lists, color):
        if self.primitive_parts == None:
            self.color_nr = len(color)
            self.primitive_parts = []
        self.levels = len(vertices_lists)

        for i in range(self.levels):
            vertex_array = []
            color_array = []
            if len(self.primitive_parts) <= i:
                self.coord_nr[i] = len(vertices_lists[i][0])

            vertex_nr = len(vertices_lists[i])
            for vertex in vertices_lists[i]:
                for coord in vertex:
                    vertex_array.append(coord)
            if len(vertex_array) != vertex_nr * self.coord_nr[i]:
                print "Incorrect vertex list"
                self.primitive_parts = None
                return

            for j in range(vertex_nr):
                for c in color:
                    color_array.append(c)
            if len(color_array) != vertex_nr * self.color_nr:
                print "Incorrect colors list"
                self.primitive = None
                return

            if len(self.primitive_parts) <= i:
                self.primitive_parts.append(
                    pyglet.graphics.vertex_list(vertex_nr,
                            ('v' + str(self.coord_nr[i]) + 'f', vertex_array),
                            ('c' + str(self.color_nr) + 'f', color_array)))
            else:
                self.primitive_parts[i].resize(vertex_nr)
                self.primitive_parts[i].vertices = vertex_array
                self.primitive_parts[i].colors = color_array


class CircleOutline(Outline):
    points = 60
    angle_step = math.pi * 2 / points

    def __init__(self, x, y, start_radius, delta_radius, color):
        self.draw(x, y, start_radius, delta_radius, color)


    def draw(self, x, y, start_radius, delta_radius, color):
        levels = int(abs(delta_radius) + 1)
        vertices_lists = []

        for i in range(levels):
            radius = start_radius + i

            vertex_array = []
            color_array = []

            for j in range(self.points):
                w = radius * math.cos(self.angle_step * j)
                h = radius * math.sin(self.angle_step * j)

                vertex_array.append((x + w, y + h))

            vertices_lists.append(vertex_array)

        super(CircleOutline, self).draw(vertices_lists, color)


class Polygon(Outline):
    primitive = None

    def __init__(self, vertices, color):
        self.draw(vertices, color)

    def render(self):
        super(Polygon, self).render(pyglet.gl.GL_POLYGON)

    def draw(self, vertices, color):
        super(Polygon, self).draw([vertices], color)


class Rect(Polygon):
    def __init__(self, x, y, width, height, color):
        self.draw(x, y, width, height, color)

    def draw(self, x, y, width, height, color):
        vertices = [(x, y),
                    (x + width, y),
                    (x + width, y + height),
                    (x, y + height)]

        super(Rect, self).draw(vertices, color)


class Circle(Polygon):
    points = 60
    angle_step = math.pi * 2 / points

    def __init__(self, x, y, radius, color):
        self.draw(x, y, radius, color)


    def draw(self, x, y, radius, color):
        vertices = []

        for i in range(self.points):
            w = radius * math.cos(self.angle_step * i)
            h = radius * math.sin(self.angle_step * i)

            vertices.append((x + w, y + h))

        super(Circle, self).draw(vertices, color)


class RoundedRect(Polygon):
    big_offset = [(0, 0), (1, 0), (1, 1), (0, 1)]
    small_offset = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
    corner_points = 20
    angle_step = math.pi / 2 / corner_points

    def __init__(self, x, y, width, height, corner_radius, color):
        self.draw(x, y, width, height, corner_radius, color)

    def draw(self, x, y, width, height, corner_radius, color):
        vertices = []

        for i in range(4):
            start_x = x + width * self.big_offset[i][0] + corner_radius * self.small_offset[i][0]
            start_y = y + height * self.big_offset[i][1] + corner_radius * self.small_offset[i][1]

            for j in range(self.corner_points):
                if i == 1 or i == 3: alfa = self.corner_points - j
                else: alfa = j

                w = corner_radius * math.cos(self.angle_step * alfa)
                h = corner_radius * math.sin(self.angle_step * alfa)
                vertices.append((start_x - w * self.small_offset[i][0],
                                 start_y - h * self.small_offset[i][1]))

        super(RoundedRect, self).draw(vertices, color)


class RoundedLabel(RoundedRect):
    label = None
    def __init__(self, x, y, width, height, corner_radius, color,
                    text, text_proportion, font, text_color):
        self.draw(x, y, width, height, corner_radius, color,
                    text, text_proportion, font, text_color)

    def render(self):
        super(RoundedLabel, self).render()
        self.label.draw()

    def draw(self, x, y, width, height, corner_radius, color,
                    text, text_proportion, font, text_color):
        super(RoundedLabel, self).draw(x, y, width, height, corner_radius, color)

        tx_size = height * text_proportion
        offset_x = x + width / 2
        offset_y = y + height / 2
        self.label = pyglet.text.Label(text, font_name = font,
                                        font_size = tx_size, bold = True,
                                        color = text_color,
                                        x = offset_x, y = offset_y,
                                        anchor_x = 'center', anchor_y = 'center')


if __name__ == '__main__':
    "Please do not run this file directly, include it."
