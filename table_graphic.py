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
        for triangle in self.triangles:
            triangle.render()

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

        il_offset_x = []
        il_offset_y = []
        for i in range(2):
            il_offset_x.append(gl_offset_x + temp_width * i + inner_border_thickness * (2 * i + 1))
            il_offset_y.append(gl_offset_y + inner_border_thickness)
            vertex_array = [(il_offset_x[i], il_offset_y[i]),
                            (il_offset_x[i] + temp_width, il_offset_y[i]),
                            (il_offset_x[i] + temp_width, il_offset_y[i] + temp_height),
                            (il_offset_x[i], il_offset_y[i] + temp_height)]

            if init:
                self.halves_3d.append(primitives.Polygon(v = vertex_array,
                                                    color = conf.TABLE_HALF_3D_COLOR))
            else:
                self.halves_3d[i].v = vertex_array


        # Draw table halves backgrounds.
        inner_3d_thickness = self.table_width * conf.INNER_3D_THICKNESS
        thickness = inner_border_thickness + inner_3d_thickness
        temp_width = temp_width - inner_3d_thickness * 2
        temp_height = temp_height - inner_3d_thickness * 2

        if init:
            self.halves_bg = []

        hv_offset_x = []
        hv_offset_y = []
        for i in range(2):
            hv_offset_x.append(gl_offset_x + temp_width * i + thickness * (2 * i + 1))
            hv_offset_y.append(gl_offset_y + thickness)
            vertex_array = [(hv_offset_x[i], hv_offset_y[i]),
                            (hv_offset_x[i] + temp_width, hv_offset_y[i]),
                            (hv_offset_x[i] + temp_width, hv_offset_y[i] + temp_height),
                            (hv_offset_x[i], hv_offset_y[i] + temp_height)]

            if init:
                self.halves_bg.append(primitives.Polygon(v = vertex_array,
                                                    color = conf.TABLE_HALF_BG_COLOR))
            else:
                self.halves_bg[i].v = vertex_array

        # Draw triangles.
        draw_color = 0
        colors = [conf.TABLE_TRIANGLE_BLACK_COLOR, conf.TABLE_TRIANGLE_RED_COLOR]
        triangle_width = temp_width / 6
        triangle_spacing = triangle_width * conf.TRIANGLE_SPACING
        triangle_height = temp_height * conf.TRIANGLE_HEIGHT
        triangle_pos = 1

        trq_offset_x = []
        trq_offset_y = []
        if init:
            self.triangles = []

        for i in range(2):
            trh_offset_y = i * temp_height
            print trh_offset_y

            for j in range(2):
                trq_offset_x.append(hv_offset_x[j])
                trq_offset_y.append(hv_offset_y[j] + trh_offset_y)

                for k in range(6):
                    vertex_array = [(trq_offset_x[i*2 + j] + triangle_width * k + triangle_spacing ,
                                     trq_offset_y[i*2 + j]) ,
                                     (trq_offset_x[i*2 + j] + triangle_width * (k + 1) - triangle_spacing,
                                     trq_offset_y[i*2 + j]) ,
                                     (trq_offset_x[i*2 + j] + triangle_width * (k + 0.5),
                                     (trq_offset_y[i*2 + j] + triangle_height * triangle_pos))]

                    if init:
                        self.triangles.append(primitives.Polygon(v = vertex_array,
                                            color = colors[draw_color]))
                    else:
                        self.triangles[i * 12 + j * 6 + k].v = vertex_array

                    draw_color += 1
                    if draw_color > 1: draw_color = 0

            draw_color += 1
            if draw_color > 1: draw_color = 0
            triangle_pos *= -1

if __name__ == '__main__':
    print "Please import me, do not run me directly!"
