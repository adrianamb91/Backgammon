import pyglet
from pyglet.gl import *
from pyglet.graphics import *
import math

import primitives as pm

class Button(object):

    def __init__(self, configuration, x, y, width, height, text):
        self.cf = configuration
        self.text = text
        self.hover = False

        self.BG_COLOR = self.cf.BUTTON_MAIN_BG_COLOR
        self.FG_COLOR = self.cf.BUTTON_MAIN_FG_COLOR

        self.draw(x, y, width, height, True)


    def render(self):
        self.button.render()


    def draw(self, x, y, width, height, init = True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        corner_radius = height * self.cf.BUTTON_MAIN_CORNER_RADIUS

        if init:
            self.button = pm.RoundedLabel(x, y, width, height, corner_radius,
                                            self.BG_COLOR, self.text,
                                            self.cf.BUTTON_MAIN_TEXT_PROPORTION,
                                            self.cf.BUTTON_MAIN_TEXT_FONT,
                                            self.FG_COLOR)
        else:
            self.button.draw(x, y, width, height, corner_radius,
                                self.BG_COLOR, self.text,
                                self.cf.BUTTON_MAIN_TEXT_PROPORTION,
                                self.cf.BUTTON_MAIN_TEXT_FONT, self.FG_COLOR)


    def change_state(self):
        if self.hover:
            self.BG_COLOR = self.cf.BUTTON_MAIN_BG_HOVER_COLOR
            self.FG_COLOR = self.cf.BUTTON_MAIN_FG_HOVER_COLOR
        else:
            self.BG_COLOR = self.cf.BUTTON_MAIN_BG_COLOR
            self.FG_COLOR = self.cf.BUTTON_MAIN_FG_COLOR

        self.draw(self.x, self.y, self.width, self.height)


    def mouse_motion(self, x, y, dx, dy):
        over = ((self.x <= x <= self.x + self.width) and
                (self.y <= y <= self.y + self.height))

        if over:
            if not self.hover:
                self.hover = True
                self.change_state()

            return True
        else:
            if self.hover:
                self.hover = False
                self.change_state()

        return False









                
                
if __name__ == '__main__':
    "Please do not run this file directly, include it."
