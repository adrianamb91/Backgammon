import pyglet
from pyglet.gl import *
from pyglet.graphics import *
import primitives
import backgammon_config as conf
import math

class Piece(object):
    selected = False
    colors = { 'white' :
                        {'shadow' : conf.PIECE_WHITE_SHADOW_COLOR,
                         'border' : conf.PIECE_WHITE_BORDER_COLOR,
                         'inner'  : conf.PIECE_WHITE_INNER_COLOR,
                         'select' : conf.PIECE_WHITE_SELECT_COLOR},
               'black' :
                        {'shadow' : conf.PIECE_BLACK_SHADOW_COLOR,
                         'border' : conf.PIECE_BLACK_BORDER_COLOR,
                         'inner'  : conf.PIECE_BLACK_INNER_COLOR,
                         'select' : conf.PIECE_BLACK_SELECT_COLOR}}

    def __init__(self, x, y, width, color):
        self.color = color
        self.shadow_parts = []
        self.draw(x, y, width, True)

    def render(self):
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        for sh in self.shadow_parts:
            sh.draw(pyglet.gl.GL_LINE_LOOP)
        pyglet.gl.glDisable(pyglet.gl.GL_BLEND)

        for part in self.parts:
            part.render()

    def draw(self, x, y, width, init = False):
        self.x = x
        self.y = y
        self.width = width
        piece_width = []
        self.piece_shadow_thickness = width * conf.PIECE_SHADOW_THICKNESS
        piece_width.append(width - self.piece_shadow_thickness)
        piece_shadow = width
        piece_border = piece_width[0] * conf.PIECE_BORDER_THICKNESS
        piece_width.append(piece_width[0] - piece_border * 2)
        piece_width.append(piece_width[0] * conf.PIECE_MIDDLE_THICKNESS)


        self.draw_shadow(x, y, self.colors[self.color]['shadow'], piece_shadow,
                            piece_width[0])

        if init:
            self.parts = []

        if init:

            self.parts.append(primitives.Circle(x = x, y = y,
                                    width = piece_width[0],
                                    color = self.colors[self.color]['border'],
                                    stroke = 0))

            self.parts.append(primitives.Circle(x = x, y = y,
                                    width = piece_width[1],
                                    color = self.colors[self.color]['inner'],
                                    stroke = 0))

            self.parts.append(primitives.Circle(x = x, y = y,
                                    width = piece_width[2],
                                    color = self.colors[self.color]['border'],
                                    stroke = 0))
        else:
            for i in range(3):
                self.parts[i].width = piece_width[i]
                self.parts[i].x = x
                self.parts[i].y = y

    def mouse_motion(self, x, y, dx, dy):
        radius = (self.width / 2) ** 2
        dist = (x - self.x) * (x - self.x) + (y - self.y) * (y - self.y)
        if dist < radius:
            if not self.selected:
                self.selected = True
                self.draw_shadow(self.x, self.y, self.colors[self.color]['select'],
                            self.width, self.width - self.piece_shadow_thickness)
        else:
            if self.selected:
                self.selected = False
                self.draw_shadow(self.x, self.y, self.colors[self.color]['shadow'],
                            self.width, self.width - self.piece_shadow_thickness)

    def draw_shadow(self, x, y, color, start_width, end_width):
        for sh in self.shadow_parts:
            sh.delete()
        self.shadow_parts = []

        point_nr = 360
        angle_step = math.pi * 2 / point_nr

        if start_width < end_width:
            start_width, end_width = end_width, start_width
        d_width = start_width - end_width + 5
        levels = (int) (d_width + 1)
        width_step = (d_width / levels) / 2

        vertex_array = []
        color_array = []

        shadow_step = conf.PIECE_SHADOW_MAX / levels

        for i in range(levels):
            shadow_value = (shadow_step * i) ** conf.PIECE_SHADOW_POWER
            radius = start_width / 2 - i * width_step

            vertex_array = []
            color_array = []

            for j in range(point_nr):
                w = radius * math.cos(angle_step * j)
                h = radius * math.sin(angle_step * j)

                vertex_array.append(x + w)
                vertex_array.append(y + h)
                for k in range(3):
                    color_array.append(color[k])
                color_array.append(shadow_value)

            self.shadow_parts.append(
                pyglet.graphics.vertex_list(point_nr,
                                            ('v2f', vertex_array),
                                            ('c4f', color_array)))

if __name__ == '__main__':
    print "Please import me, do not run me directly!"
