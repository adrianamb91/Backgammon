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


