import pyglet
from pyglet.gl import *
import primitives
import backgammon_config as conf
import math
import piece_graphic as piece


class Table(object):
    def __init__(self, width, height):
        self.offset_x = {}
        self.offset_y = {}
        self.temp_width = {}
        self.temp_height = {}

        self.draw(width, height, True)

    def render(self):
        self.background.render()
        self.table_border.render()
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
        for p in self.pieces:
            p.render()

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

        self.draw_canvas(init)
        self.draw_table_border(init)
        self.draw_table_3d(init)
        self.draw_table_halves(init)
        self.draw_table_triangles(init)
        self.draw_table_home_labels(init)
        self.draw_pieces(init)

    def draw_pieces(self, init = False):
        width = self.temp_width['triangle']

        offset_x_pc = self.offset_x['half'][0] + width / 2
        offset_y_px = self.offset_y['half'][1] + width / 2

        if init:
            self.pieces = []
            self.pieces.append(piece.Piece(200, 200, width, 'white'))
            self.pieces.append(piece.Piece(400, 200, width, 'black'))
        else:
            self.pieces[0].draw(200, 200, width)
            self.pieces[1].draw(400, 200, width)

    def draw_canvas(self, init = False):
        vertex_array = [(0, 0),
                        (self.width, 0),
                        (self.width, self.height),
                        (0, self.height)]
        if init:
            self.background = primitives.Polygon(v = vertex_array,
                                        color = conf.BG_COLOR, style = 0)
        else:
            self.background.v = vertex_array

    def draw_table_border(self, init = False):
        self.offset_x['global'] = (self.width - self.table_width) / 2
        self.offset_y['global'] = (self.height - self.table_height) / 2

        vertex_array = [(self.offset_x['global'], self.offset_y['global']),
                        (self.offset_x['global'] + self.table_width,
                            self.offset_y['global']),
                        (self.offset_x['global'] + self.table_width,
                            self.offset_y['global'] + self.table_height),
                        (self.offset_x['global'], 
                            self.offset_y['global'] + self.table_height)]
        if init:
            self.table_border = primitives.Polygon(v = vertex_array,
                                                color = conf.TABLE_BORDER_COLOR)
        else:
            self.table_border.v = vertex_array

    def draw_table_3d(self, init = False):
        self.inner_border_thickness = self.table_width * conf.INNER_BORDER_THICKNESS
        self.temp_width['illusion'] = self.table_width / 2 - self.inner_border_thickness * 2
        self.temp_height['illusion'] = self.table_height - self.inner_border_thickness * 2

        if init:
            self.halves_3d = []

        for i in range(2):
            offset_x_il = self.offset_x['global'] + self.temp_width['illusion'] * i + self.inner_border_thickness * (2 * i + 1)
            offset_y_il = self.offset_y['global'] + self.inner_border_thickness
            vertex_array = [(offset_x_il, offset_y_il),
                            (offset_x_il + self.temp_width['illusion'], 
                                offset_y_il),
                            (offset_x_il + self.temp_width['illusion'], 
                                offset_y_il + self.temp_height['illusion']),
                            (offset_x_il, 
                                offset_y_il + self.temp_height['illusion'])]

            if init:
                self.halves_3d.append(primitives.Polygon(v = vertex_array,
                                                    color = conf.TABLE_HALF_3D_COLOR))
            else:
                self.halves_3d[i].v = vertex_array

    def draw_table_halves(self, init = False):
        inner_3d_thickness = self.table_width * conf.INNER_3D_THICKNESS
        thickness = self.inner_border_thickness + inner_3d_thickness
        self.temp_width['half'] = self.temp_width['illusion'] - inner_3d_thickness * 2
        self.temp_height['half'] = self.temp_height['illusion'] - inner_3d_thickness * 2

        if init:
            self.halves_bg = []

        self.offset_x['half'] = []
        self.offset_y['half'] = []
        for i in range(2):
            self.offset_x['half'].append(self.offset_x['global'] + self.temp_width['half'] * i + thickness * (2 * i + 1))
            self.offset_y['half'].append(self.offset_y['global'] + thickness)
            vertex_array = [(self.offset_x['half'][i], self.offset_y['half'][i]),
                            (self.offset_x['half'][i] + self.temp_width['half'],
                                self.offset_y['half'][i]),
                            (self.offset_x['half'][i] + self.temp_width['half'],
                                self.offset_y['half'][i] + self.temp_height['half']),
                            (self.offset_x['half'][i],
                                self.offset_y['half'][i] + self.temp_height['half'])]

            if init:
                self.halves_bg.append(primitives.Polygon(v = vertex_array,
                                                    color = conf.TABLE_HALF_BG_COLOR))
            else:
                self.halves_bg[i].v = vertex_array

    def draw_table_triangles(self, init = False):
        draw_color = 0
        colors = [conf.TABLE_TRIANGLE_BLACK_COLOR, conf.TABLE_TRIANGLE_RED_COLOR]
        self.temp_width['triangle'] = self.temp_width['half'] / 6
        triangle_spacing = self.temp_width['triangle'] * conf.TRIANGLE_SPACING
        self.temp_height['triangle'] = self.temp_height['half'] * conf.TRIANGLE_HEIGHT
        triangle_pos = 1

        self.offset_x['tr_quarter'] = []
        self.offset_y['tr_quarter'] = []
        if init:
            self.triangles = []

        for i in range(2):
            offset_y_trh = i * self.temp_height['half']

            for j in range(2):
                self.offset_x['tr_quarter'].append(self.offset_x['half'][j])
                self.offset_y['tr_quarter'].append(self.offset_y['half'][j] + offset_y_trh)

                for k in range(6):
                    vertex_array = [(self.offset_x['tr_quarter'][i*2 + j] + self.temp_width['triangle'] * k + triangle_spacing ,
                                        self.offset_y['tr_quarter'][i*2 + j]) ,
                                     (self.offset_x['tr_quarter'][i*2 + j] + self.temp_width['triangle'] * (k + 1) - triangle_spacing,
                                        self.offset_y['tr_quarter'][i*2 + j]) ,
                                     (self.offset_x['tr_quarter'][i*2 + j] + self.temp_width['triangle'] * (k + 0.5),
                                        self.offset_y['tr_quarter'][i*2 + j] + self.temp_height['triangle'] * triangle_pos)]

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

    def draw_table_home_labels(self, init = False):
        #Draw home labels background.
        label_width = self.table_width * conf.HOME_LABEL_WIDTH
        label_height = self.inner_border_thickness * conf.HOME_LABEL_HEIGHT

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

            offset_x_lb = self.offset_x['global'] + self.table_width * conf.HOME_LABEL_SPACER
            offset_y_lb = self.offset_y['global'] + self.table_height * k - self.inner_border_thickness * k + (self.inner_border_thickness - label_height) / 2

            for i in range(4):
                start_x = offset_x_lb + label_width * big_offset[i][0] + corner_radius * small_offset[i][0]
                start_y = offset_y_lb + label_height * big_offset[i][1] + corner_radius * small_offset[i][1]

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

            offset_x_tx = offset_x_lb + label_width / 2
            offset_y_tx = offset_y_lb + label_height / 2
            tx_size = label_height * conf.HOME_LABEL_TEXT_PROPORTION

            if init:
                self.labels_text.append(pyglet.text.Label(lb_text[k],
                                        font_name = 'Helvetica',
                                        font_size = tx_size,
                                        bold = True,
                                        color = conf.HOME_LABEL_FG_COLOR,
                                        x = offset_x_tx, y = offset_x_tx,
                                        anchor_x = 'center', anchor_y = 'center'))
            else:
                self.labels_text[k].x = offset_x_tx
                self.labels_text[k].y = offset_y_tx
                self.labels_text[k].font_size = tx_size

if __name__ == '__main__':
    print "Please import me, do not run me directly!"
