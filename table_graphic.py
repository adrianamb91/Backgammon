import pyglet
from pyglet.gl import *
import primitives
import backgammon_config as conf


class Table(object):
    def __init__(self, width, height):
        self.draw(width, height, True)

    def render(self):
        self.background.render()
        self.table_bg.render()
        for half_3d in self.halves_3d:
            half_3d.render()
        for half_bg in self.halves_bg:
            half_bg.render()

    def resize(self):
        temp_width = self.width - conf.BORDER_THICKNESS * 2
        temp_height = temp_width * conf.RELATIVE_HEIGHT / conf.RELATIVE_WIDTH
        if temp_height > self.height:
            temp_height = self.height - conf.BORDER_THICKNESS * 2
            temp_width = temp_height * conf.RELATIVE_WIDTH / conf.RELATIVE_HEIGHT

        self.table_width = temp_width
        self.table_height = temp_height

    def draw(self, w, h, init = False):
        self.width = w
        self.height = h
        self.resize()

        # Draw neutral background.
        vertex_array = [(0, 0),
                        (self.width, 0),
                        (self.width, self.height),
                        (0, self.height)]
        if init:
            self.background = primitives.Polygon(v = vertex_array,
                                        color = conf.BG_COLOR, style = 0)
        else:
            self.background.v = vertex_array

        # Draw table canvas background.
        gl_offset_x = (self.width - self.table_width) / 2
        gl_offset_y = (self.height - self.table_height) / 2

        vertex_array = [(gl_offset_x, gl_offset_y),
                        (gl_offset_x + self.table_width, gl_offset_y),
                        (gl_offset_x + self.table_width, gl_offset_y + self.table_height),
                        (gl_offset_x, gl_offset_y + self.table_height)]
        if init:
            self.table_bg = primitives.Polygon(v = vertex_array,
                                                color = conf.TABLE_BG_COLOR)
        else:
            self.table_bg.v = vertex_array

        # Draw table 3D illusion.
        inner_border_thickness = self.table_width * conf.INNER_BORDER_THICKNESS
        temp_width = self.table_width / 2 - inner_border_thickness * 2
        temp_height = self.table_height - inner_border_thickness * 2

        if init:
            self.halves_3d = []

        for i in range(2):
            offset_x = gl_offset_x + temp_width * i + inner_border_thickness * (2 * i + 1)
            offset_y = gl_offset_y + inner_border_thickness
            vertex_array = [(offset_x, offset_y),
                            (offset_x + temp_width, offset_y),
                            (offset_x + temp_width, offset_y + temp_height),
                            (offset_x, offset_y + temp_height)]

            if init:
                self.halves_3d.append(primitives.Polygon(v = vertex_array,
                                                    color = conf.TABLE_HALF_3D_COLOR))
            else:
                self.halves_3d[i].v = vertex_array


        # Draw table halves backgrounds.
        inner_3d_thickness = self.table_width * conf.INNER_3D_THICKNESS
        temp_width = temp_width - inner_3d_thickness * 2
        temp_height = temp_height - inner_3d_thickness * 2

        if init:
            self.halves_bg = []

        for i in range(2):
            offset_x = gl_offset_x + temp_width * i + (inner_border_thickness + inner_3d_thickness) * (2 * i + 1)
            offset_y = gl_offset_y + inner_border_thickness + inner_3d_thickness
            vertex_array = [(offset_x, offset_y),
                            (offset_x + temp_width, offset_y),
                            (offset_x + temp_width, offset_y + temp_height),
                            (offset_x, offset_y + temp_height)]

            if init:
                self.halves_bg.append(primitives.Polygon(v = vertex_array,
                                                    color = conf.TABLE_HALF_BG_COLOR))
            else:
                self.halves_bg[i].v = vertex_array

        # TODO: Draw triangles

if __name__ == '__main__':
    print "Please import me, do not run me directly!"
