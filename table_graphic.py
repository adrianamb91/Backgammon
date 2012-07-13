import pyglet
from pyglet.gl import *
import primitives
import backgammon_config as conf
import math


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
        for label in self.labels:
            label.render()
        for label_text in self.labels_text:
            label_text.draw()

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

        #Draw home labels.
        label_width = self.table_width * conf.HOME_LABEL_WIDTH
        label_height = inner_border_thickness * conf.HOME_LABEL_HEIGHT

        corner_radius = label_width * conf.HOME_LABEL_CORNER_RADIUS
        corner_points = (int) (corner_radius * conf.HOME_LABEL_CORNER_POINTS)
        angle_step = math.pi / 2 / corner_points

        big_offset = [(0, 0), (1, 0), (1, 1), (0, 1)]
        small_offset = [(1, 1), (-1, 1), (-1, -1), (1, -1)]

        if init:
            self.labels = []
            self.labels_text = []
            lb_text = ["Your home", "Opponent home"]

        for k in range(2):
            vertex_array = []

            lb_offset_x = gl_offset_x + self.table_width * conf.HOME_LABEL_SPACER
            lb_offset_y = gl_offset_y + self.table_height * k - inner_border_thickness * k + (inner_border_thickness - label_height) / 2

            for i in range(4):
                start_x = lb_offset_x + label_width * big_offset[i][0] + corner_radius * small_offset[i][0]
                start_y = lb_offset_y + label_height * big_offset[i][1] + corner_radius * small_offset[i][1]

                for j in range(corner_points):
                    if i == 1 or i == 3: alfa = corner_points - j
                    else: alfa = j

                    w = corner_radius * math.cos(angle_step * alfa)
                    h = corner_radius * math.sin(angle_step * alfa)
                    vertex_array.append((start_x - w * small_offset[i][0],
                                         start_y - h * small_offset[i][1]))

            if init:
                self.labels.append(primitives.Polygon(v = vertex_array,
                                                color = conf.HOME_LABEL_BG_COLOR))
            else:
                self.labels[k].v = vertex_array

            tx_offset_x = lb_offset_x + label_width / 2
            tx_offset_y = lb_offset_y + label_height / 2
            tx_size = label_height * conf.HOME_LABEL_TEXT_PROPORTION

            if init:
                self.labels_text.append(pyglet.text.Label(lb_text[k],
                                        font_name = 'Helvetica',
                                        font_size = tx_size,
                                        bold = True,
                                        color = conf.HOME_LABEL_FG_COLOR,
                                        x = tx_offset_x, y = tx_offset_y,
                                        anchor_x = 'center', anchor_y = 'center'))
            else:
                self.labels_text[k].x = tx_offset_x
                self.labels_text[k].y = tx_offset_y
                self.labels_text[k].font_size = tx_size

if __name__ == '__main__':
    print "Please import me, do not run me directly!"
