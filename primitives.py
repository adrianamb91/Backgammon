import pyglet
from pyglet.gl import *
from pyglet.graphics import *
import math

class Polygon(object):
    primitive = None
    def __init__(self, vertices, color):
        self.draw(vertices, color)

    def render(self):
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        self.primitive.draw(pyglet.gl.GL_POLYGON)
        pyglet.gl.glDisable(pyglet.gl.GL_BLEND)

    def draw(self, vertices, color):
        if self.primitive != None:
            self.primitive.delete()

        vertex_array = []
        color_array = []

        vertex_nr = len(vertices)
        coord_nr = len(vertices[0])
        color_nr = len(color)

        for vertex in vertices:
            for coord in vertex:
                vertex_array.append(coord)
        if len(vertex_array) != vertex_nr * coord_nr:
            print "Incorrect vertex list"
            self.primitive = None
            return

        for i in range(vertex_nr):
            for c in color:
                color_array.append(c)

        self.primitive = pyglet.graphics.vertex_list(vertex_nr,
                                    ('v' + str(coord_nr) + 'f', vertex_array),
                                    ('c' + str(color_nr) + 'f', color_array))


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
    points = 180
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
    corner_points = 90
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
