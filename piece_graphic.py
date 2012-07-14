import pyglet
from pyglet.gl import *
from pyglet.graphics import *
import primitives
import backgammon_config as conf
import math
import gradient

class Piece(object):
    selected = False
    colors = { 'white' :
                        {'shadow_start' : conf.PIECE_WHITE_SHADOW_START_COLOR,
                         'shadow_end' : conf.PIECE_WHITE_SHADOW_END_COLOR,
                         'border' : conf.PIECE_WHITE_BORDER_COLOR,
                         'inner'  : conf.PIECE_WHITE_INNER_COLOR,
                         'select' : conf.PIECE_WHITE_SELECT_COLOR},
               'black' :
                        {'shadow_start' : conf.PIECE_BLACK_SHADOW_START_COLOR,
                         'shadow_end' : conf.PIECE_BLACK_SHADOW_END_COLOR,
                         'border' : conf.PIECE_BLACK_BORDER_COLOR,
                         'inner'  : conf.PIECE_BLACK_INNER_COLOR,
                         'select' : conf.PIECE_BLACK_SELECT_COLOR}}

    def __init__(self, x, y, width, color):
        self.color = color
        self.draw(x, y, width, True)

    def render(self):
        self.shadow.render()
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

    def mouse_motion(self, x, y, dx, dy):
        pass
#        radius = (self.width / 2) ** 2
#        dist = (x - self.x) * (x - self.x) + (y - self.y) * (y - self.y)
#        if dist < radius:
#            if not self.selected:
#                self.selected = True
#                self.draw_shadow(self.x, self.y, self.colors[self.color]['select'],
#                            self.width, self.width - self.piece_shadow_thickness)
#        else:
#            if self.selected:
#                self.selected = False
#                self.draw_shadow(self.x, self.y, self.colors[self.color]['shadow'],
#                            self.width, self.width - self.piece_shadow_thickness)

if __name__ == '__main__':
    print "Please import me, do not run me directly!"
