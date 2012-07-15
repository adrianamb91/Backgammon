import pyglet
from pyglet.gl import *
import primitives
import primitives2 as pm
import backgammon_config as conf
import math
import piece_graphic as piece
import gradient


class Table(object):
    PLAYER = 'white'
    COMPUTER = 'black'

    def __init__(self, width, height, board):
        self.board = board
        self.player_colors = { board.get_computer() : self.COMPUTER,
                               board.get_player() : self.PLAYER}
        self.offset_x = {}
        self.offset_y = {}
        self.temp_width = {}
        self.temp_height = {}

        self.draw(width, height, True)


    def mouse_motion(self, x, y, dx, dy):
        for col in self.pieces:
            for p in col:
                if p.mouse_motion(x, y, dx, dy):
                    return True


    def mouse_press_left(self, x, y):
        for col in self.pieces:
            for p in col:
                p.mouse_press_left(x, y)


    def render(self):
        self.background.render()

        self.table_border.render()
        self.table_border_shadow.render()

        for half_3d in self.halves_3d:
            half_3d.render()
        for half_bg in self.halves_bg:
            half_bg.render()
        for triangle in self.triangles:
            triangle.render()
        for half_bg_shadow in self.halves_bg_shadow:
            half_bg_shadow.render()

        for label in self.labels:
            label.render()
        for label_text in self.labels_text:
            label_text.draw()

        for col in self.pieces:
            for p in col:
                p.render_effects()
        for col in self.pieces:
            for p in col:
                p.render()
        for col in self.pieces:
            for p in col:
                p.render_extras()


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


    def resize(self):
        temp_width = self.width - conf.BORDER_THICKNESS * 2
        temp_height = temp_width * conf.RELATIVE_HEIGHT / conf.RELATIVE_WIDTH
        if temp_height > self.height:
            temp_height = self.height - conf.BORDER_THICKNESS * 2
            temp_width = temp_height * conf.RELATIVE_WIDTH / conf.RELATIVE_HEIGHT

        self.table_width = temp_width
        self.table_height = temp_height


    def draw_pieces(self, init = False):
        width = self.temp_width['triangle'] * conf.PIECE_SIZE_PERCENTAGE
        shadow_thickness = width * conf.PIECE_SHADOW_THICKNESS
        actual_width = width - shadow_thickness + 1

        if init:
            self.pieces = []
            self.pieces.append([])
            spaces = self.board.get_spaces()

        for i in range(1, 25):
            if init: 
                self.pieces.append([])
                piece_nr = spaces[i][0]
            else:
                piece_nr = len(self.pieces[i])

            for j in range(piece_nr):
                pos = (i - 1)
                if 0 <= pos <= 5 or 18 <= pos <= 23:
                    half = 0
                else: half = 1
                factor_w = pos % 6

                if pos < 12:
                    offset_x_pc = self.offset_x['half'][half] + self.temp_width['triangle'] / 2 + self.temp_width['triangle'] * factor_w
                    offset_y_pc = self.offset_y['half'][half] + actual_width / 2 + actual_width * j
                else:
                    offset_x_pc = self.offset_x['half'][half] + self.temp_width['half'] - self.temp_width['triangle'] / 2 - self.temp_width['triangle'] * factor_w
                    offset_y_pc = self.offset_y['half'][half] + self.temp_height['half'] - actual_width / 2 - actual_width * j

                if init:
                    self.pieces[i].append(
                        piece.Piece(
                            offset_x_pc, offset_y_pc, width, self.player_colors[spaces[i][1]],
                            j == piece_nr - 1 and self.player_colors[spaces[i][1]] == self.PLAYER))
                else:
                    self.pieces[i][j].draw(offset_x_pc, offset_y_pc, width,
                            j == piece_nr - 1 and self.pieces[i][j].color == self.PLAYER)

            if init: self.pieces.append([])


    def draw_canvas(self, init = False):
        if init:
            self.background = pm.Rect(0, 0, self.width, self.height, conf.BG_COLOR)
        else:
            self.background.draw(0, 0, self.width, self.height, conf.BG_COLOR)


    def draw_table_border(self, init = False):
        self.offset_x['global'] = (self.width - self.table_width) / 2
        self.offset_y['global'] = (self.height - self.table_height) / 2
        self.inner_border_thickness = self.table_width * conf.INNER_BORDER_THICKNESS
        gradient_end = self.inner_border_thickness * conf.TABLE_BORDER_SHADOW_THICKNESS

        if init:
            self.table_border = pm.Rect(self.offset_x['global'],
                                        self.offset_y['global'],
                                        self.table_width,
                                        self.table_height,
                                        conf.TABLE_BORDER_COLOR)

            self.table_border_shadow = gradient.RectGradient(
                                self.offset_x['global'], self.offset_y['global'],
                                self.table_width, self.table_height,
                                conf.TABLE_BORDER_SHADOW_START_COLOR,
                                conf.TABLE_BORDER_SHADOW_END_COLOR,
                                0, gradient_end)

        else:
            self.table_border.draw(self.offset_x['global'],
                                    self.offset_y['global'],
                                    self.table_width,
                                    self.table_height,
                                    conf.TABLE_BORDER_COLOR)

            self.table_border_shadow.draw(
                                self.offset_x['global'], self.offset_y['global'],
                                self.table_width, self.table_height,
                                0, gradient_end)


    def draw_table_3d(self, init = False):
        self.temp_width['illusion'] = self.table_width / 2 - self.inner_border_thickness * 2
        self.temp_height['illusion'] = self.table_height - self.inner_border_thickness * 2
        self.inner_3d_thickness = self.table_width * conf.INNER_3D_THICKNESS

        if init:
            self.halves_3d = []

        for i in range(2):
            offset_x_il = self.offset_x['global'] + self.temp_width['illusion'] * i + self.inner_border_thickness * (2 * i + 1)
            offset_y_il = self.offset_y['global'] + self.inner_border_thickness

            if init:
                self.halves_3d.append(gradient.RectGradient(
                                offset_x_il, offset_y_il,
                                self.temp_width['illusion'], self.temp_height['illusion'],
                                conf.TABLE_HALF_3D_SHADOW_START_COLOR,
                                conf.TABLE_HALF_3D_SHADOW_END_COLOR,
                                0, self.inner_3d_thickness))
            else:
                self.halves_3d[i].draw(offset_x_il, offset_y_il,
                                self.temp_width['illusion'], self.temp_height['illusion'],
                                0, self.inner_3d_thickness)


    def draw_table_halves(self, init = False):
        thickness = self.inner_border_thickness + self.inner_3d_thickness
        self.temp_width['half'] = self.temp_width['illusion'] - self.inner_3d_thickness * 2
        self.temp_height['half'] = self.temp_height['illusion'] - self.inner_3d_thickness * 2
        if self.temp_width['half'] < self.temp_height['half']:
            gradient_end = self.temp_width['half'] * conf.TABLE_HALF_BG_SHADOW_THICKNESS
        else:
            gradient_end = self.temp_height['half'] * conf.TABLE_HALF_BG_SHADOW_THICKNESS

        if init:
            self.halves_bg = []
            self.halves_bg_shadow = []

        self.offset_x['half'] = []
        self.offset_y['half'] = []
        for i in range(2):
            self.offset_x['half'].append(self.offset_x['global'] + self.temp_width['half'] * i + thickness * (2 * i + 1))
            self.offset_y['half'].append(self.offset_y['global'] + thickness)

            if init:
                self.halves_bg.append(pm.Rect(self.offset_x['half'][i],
                                                self.offset_y['half'][i],
                                                self.temp_width['half'],
                                                self.temp_height['half'],
                                                conf.TABLE_HALF_BG_COLOR))

                self.halves_bg_shadow.append(gradient.RectGradient(
                                self.offset_x['half'][i], self.offset_y['half'][i],
                                self.temp_width['half'], self.temp_height['half'],
                                conf.TABLE_HALF_BG_SHADOW_START_COLOR,
                                conf.TABLE_HALF_BG_SHADOW_END_COLOR,
                                0, gradient_end))
            else:
                self.halves_bg[i].draw(self.offset_x['half'][i],
                                        self.offset_y['half'][i],
                                        self.temp_width['half'],
                                        self.temp_height['half'],
                                        conf.TABLE_HALF_BG_COLOR)

                self.halves_bg_shadow[i].draw(
                                self.offset_x['half'][i], self.offset_y['half'][i],
                                self.temp_width['half'], self.temp_height['half'],
                                0, gradient_end)


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
                        self.triangles.append(pm.Polygon(vertex_array,
                                                        colors[draw_color]))
                    else:
                        self.triangles[i * 12 + j * 6 + k].draw(
                                                        vertex_array,
                                                        colors[draw_color])

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
    "Please import me, do not run me directly!"
