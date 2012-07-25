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
        self.pressed = False

        self.BG_COLOR = self.cf.BUTTON_BG_COLOR
        self.FG_COLOR = self.cf.BUTTON_FG_COLOR

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
                                            self.cf.BUTTON_TEXT_PROPORTION,
                                            self.cf.BUTTON_TEXT_FONT,
                                            self.FG_COLOR)
        else:
            self.button.draw(x, y, width, height, corner_radius,
                                self.BG_COLOR, self.text,
                                self.cf.BUTTON_TEXT_PROPORTION,
                                self.cf.BUTTON_TEXT_FONT, self.FG_COLOR)


    def change_state(self):
        if self.pressed:
            self.BG_COLOR = self.cf.BUTTON_BG_PRESS_COLOR
            self.FG_COLOR = self.cf.BUTTON_FG_PRESS_COLOR
        elif self.hover:
            self.BG_COLOR = self.cf.BUTTON_BG_HOVER_COLOR
            self.FG_COLOR = self.cf.BUTTON_FG_HOVER_COLOR
        else:
            self.BG_COLOR = self.cf.BUTTON_BG_COLOR
            self.FG_COLOR = self.cf.BUTTON_FG_COLOR

        self.draw(self.x, self.y, self.width, self.height)


    def is_over(self, x, y):
        return ((self.x <= x <= self.x + self.width) and
                (self.y <= y <= self.y + self.height))

    def mouse_motion(self, x, y, dx, dy):
        over = self.is_over(x, y)

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

    def mouse_press_left(self, x, y):
        over = self.is_over(x, y)

        if over:
            self.pressed = True
            self.change_state()
        else:
            if self.pressed:
                self.pressed = False
                self.change_state()

    def mouse_release_left(self, x, y):
        over = self.is_over(x, y)

        if self.pressed:
            self.pressed = False
            self.change_state()

            if over:
                return True

        return False

if __name__ == '__main__':
    "Please do not run this file directly, include it."
