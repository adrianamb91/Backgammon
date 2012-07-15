import pyglet
from pyglet.gl import *
from pyglet.graphics import *
import primitives
import backgammon_config as conf
import math
import gradient

class Piece(object):
    NONE = conf.PIECE_SELECTOR_NONE
    HOVER = conf.PIECE_SELECTOR_HOVER
    SELECTED = conf.PIECE_SELECTOR_SELECTED
    CURRENT = conf.PIECE_SELECTOR_NONE

    hover = False
    selected = False
    colors = { 'white' :
                        {'shadow_start' : conf.PIECE_WHITE_SHADOW_START_COLOR,
                         'shadow_end' : conf.PIECE_WHITE_SHADOW_END_COLOR,
                         'border' : conf.PIECE_WHITE_BORDER_COLOR,
                         'inner'  : conf.PIECE_WHITE_INNER_COLOR},
               'black' :
                        {'shadow_start' : conf.PIECE_BLACK_SHADOW_START_COLOR,
                         'shadow_end' : conf.PIECE_BLACK_SHADOW_END_COLOR,
                         'border' : conf.PIECE_BLACK_BORDER_COLOR,
                         'inner'  : conf.PIECE_BLACK_INNER_COLOR}}

    def __init__(self, x, y, width, color):
        self.color = color
        self.selector_parts = []
        self.draw(x, y, width, True)

    def render(self):
        self.shadow.render()
        for part in self.parts:
            part.render()

        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        for part in self.selector_parts:
            part.draw(pyglet.gl.GL_LINE_LOOP)
        pyglet.gl.glDisable(pyglet.gl.GL_BLEND)

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

        if init:
            self.shadow = gradient.CircularGradient(x, y,
                                        self.colors[self.color]['shadow_start'],
                                        self.colors[self.color]['shadow_end'],
                                        piece_width[0] / 2,
                                        piece_shadow / 2)
        else:
            self.shadow.draw(x, y, piece_shadow / 2, piece_width[0] / 2)


        if init:
            self.parts = []
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

        self.draw_selector()

    def draw_selector(self):
        for part in self.selector_parts:
            part.delete()
        self.selector_parts = []
        
        start_radius = (self.width + self.width * conf.PIECE_SELECTOR_SPACING) / 2
        delta_radius = self.width * conf.PIECE_SELECTOR_THICKNESS

        levels = int(abs(delta_radius) + 1)
        radius_step = 1

        points = 360
        angle_step = math.pi * 2 / points

        vertex_array = []
        color_array = []

        for i in range(levels):
            radius = start_radius + i * radius_step
            vertex_array = []
            color_array = []

            for j in range(points):
                w = radius * math.cos(angle_step * j)
                h = radius * math.sin(angle_step * j)

                vertex_array.append(self.x + w)
                vertex_array.append(self.y + h)
                for c in self.CURRENT:
                    color_array.append(c)

            self.selector_parts.append(
                pyglet.graphics.vertex_list(points,
                                            ('v2f', vertex_array),
                                            ('c4f', color_array)))

    def mouse_motion(self, x, y, dx, dy):
        radius = (self.width / 2) ** 2
        dist = (x - self.x) * (x - self.x) + (y - self.y) * (y - self.y)

        if dist < radius:
            if not self.hover:
                self.hover = True
                self.CURRENT = Piece.HOVER
                self.draw_selector()
        else:
            if self.hover:
                self.hover = False
                self.CURRENT = Piece.NONE
                self.draw_selector()

        if self.hover: return True
        else: return False

if __name__ == '__main__':
    print "Please import me, do not run me directly!"
