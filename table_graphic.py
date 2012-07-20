import pyglet

import primitives as pm
import gradient as gr
import piece_graphic as piece

import table_graphic_config as cf

                #TODO add piece borning suggestion
                #TODO actual movement of piece when suggestion is clicked

class Table(object):
    PLAYER = 'white'
    COMPUTER = 'black'
    GHOST = 'ghost'

    PIECE_NORMAL = 0
    PIECE_BAR = 1
    PIECE_BORNE = 2
    PIECE_GHOST = 3

    animated = []
    offset_x = {}
    offset_y = {}
    temp_width = {}
    temp_height = {}
    suggestions = set()

    dice_drawing = { 1: [(1, 1)],
                     2: [(0, 2), (2, 0)],
                     3: [(0, 2), (1, 1), (2, 0)],
                     4: [(0, 0), (0, 2), (2, 0), (2, 2)],
                     5: [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)],
                     6: [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)]}

    def __init__(self, width, height, board):
        self.board = board
        self.player_colors = { board.get_computer() : Table.COMPUTER,
                               board.get_player() : Table.PLAYER}

        self.board.generate_dices()
        self.draw(width, height, True)

        pyglet.clock.schedule_interval(self.animate_pieces, cf.TICK_SIZE)


    def mouse_motion(self, x, y, dx, dy):
        for p in self.active_pieces:
            if p.mouse_motion(x, y, dx, dy):
                return True

        for p in self.active_ghosts:
            if p.mouse_motion(x, y, dx, dy):
                return True


    def mouse_press_left(self, x, y):
        col = None
        for i in range(len(self.game_pieces)):
            for j in range(len(self.game_pieces[i])):
                if self.game_pieces[i][j].mouse_press_left(x, y):
                    col = i

        for bar in self.bar_pieces:
            for p in bar:
                if p.mouse_press_left(x, y):
                    col = -1

        if col != None:
            suggestions = self.board.get_player_destinations(col + 1)
            self.suggestions = set([s - 1 for s in suggestions])
        else: self.suggestions = set()

        self.draw_ghosts()


    def animate_pieces(self, dt):
        for p in self.animated:
            piece = p[0]
            piece.draw(piece.x - p[1], piece.y - p[2], piece.total_width - p[3], False)
            piece.render()
            p[4] -= 1

        self.animated[:] = [x for x in self.animated if x[4] > 0]


    def move_piece(self, piece, x, y, width):
        for p in self.animated:
            if piece == p[0]:
                return
        dx = piece.x - x
        dy = piece.y - y
        dw = piece.total_width - width

        steps = cf.PIECE_ANIMATION_STEPS
        step_x = dx / steps
        step_y = dy / steps
        step_w = dw / steps

        self.animated.append([piece, step_x, step_y, step_w, steps])


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

        for dice in self.dices:
            dice.render()
        for point in self.active_points:
            point.render()

        for p in self.active_pieces:
            p.render_effects()
        for p in self.active_pieces:
            p.render()
        for p in self.active_pieces:
            p.render_extras()

        for p in self.active_ghosts:
            p.render_effects()
        for p in self.active_ghosts:
            p.render()
        for p in self.active_ghosts:
            p.render_extras()

        for col in self.borne_pieces:
            for p in col:
                p.render_effects()
        for col in self.borne_pieces:
            for p in col:
                p.render()


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
        self.draw_dices(init)
        self.draw_pieces(init)
        self.draw_ghosts(init)


    def resize(self):
        temp_width = self.width - cf.BORDER_THICKNESS * 2
        temp_height = temp_width * cf.RELATIVE_HEIGHT / cf.RELATIVE_WIDTH
        if temp_height > self.height:
            temp_height = self.height - cf.BORDER_THICKNESS * 2
            temp_width = temp_height * cf.RELATIVE_WIDTH / cf.RELATIVE_HEIGHT

        self.table_width = temp_width
        self.table_height = temp_height


    def draw_pieces(self, init = False):
        if init:
            self.piece_pool = []
            for i in range(30):
                self.piece_pool.append(piece.Piece(cf, 0, 0, 1, Table.PLAYER,
                                                                        False))

        if not init:
            for p in self.active_pieces:
                self.piece_pool.append(p)
            for col in self.borne_pieces:
                for p in col:
                    self.piece_pool.append(p)

        self.active_pieces = []
        self.game_pieces = []
        for i in range(24): self.game_pieces.append([])
        self.bar_pieces = [[], []]
        self.borne_pieces = [[], []]

        spaces = self.board.get_spaces()
        piece_index = { self.board.get_player() : 0,
                        self.board.get_computer() : 0}

        for i in range(1, 25):
            piece_nr = spaces[i][0]

            for j in range(piece_nr):
                pos = (i - 1)
                self.draw_piece(self.piece_pool, self.game_pieces[pos],
                                self.active_pieces, Table.PIECE_NORMAL,
                                self.player_colors[spaces[i][1]],
                                (j == piece_nr - 1 and
                                self.player_colors[spaces[i][1]] == Table.PLAYER),
                                pos)
                piece_index[spaces[i][1]] += 1

        for i in range(2):
            for j in range(spaces[0][i * 2]):
                self.draw_piece(self.piece_pool, self.bar_pieces[i],
                                self.active_pieces, Table.PIECE_BAR,
                                self.player_colors[spaces[0][i * 2 + 1]],
                                (j == spaces[0][i * 2] - 1 and
                                self.player_colors[spaces[0][i * 2 + 1]] ==
                                                                Table.PLAYER))
                piece_index[spaces[0][i * 2 + 1]] += 1

        player_order = { 0: (self.board.get_player(), Table.PLAYER),
                         1: (self.board.get_computer(), Table.COMPUTER)}

        for i in range(2):
            piece_nr = 15 - piece_index[player_order[i][0]]

            for j in range(piece_nr):
                self.draw_piece(self.piece_pool, self.borne_pieces[i],
                                None, Table.PIECE_BORNE, player_order[i][1],
                                False)


    def draw_ghosts(self, init = False):
        if init:
            self.ghost_pool = []
            for i in range(30):
                self.ghost_pool.append(piece.Piece(cf, 0, 0, 1, Table.GHOST,
                                                                        False))

        if not init:
            for p in self.active_ghosts:
                self.ghost_pool.append(p)

        self.active_ghosts = []

        for pos in self.suggestions:
            self.draw_piece(self.ghost_pool, self.active_ghosts,
                            None, Table.PIECE_GHOST, Table.GHOST, True, pos)


    def draw_piece(self, source_pool, target_pool, aux_pool, style, color,
                                                        selectable, col = 0):
        # Set dimensions.
        if style == Table.PIECE_NORMAL or style == Table.PIECE_GHOST:
            width = self.temp_width['triangle'] * cf.PIECE_SIZE_PERCENTAGE
            shadow_thickness = width * cf.PIECE_SHADOW_THICKNESS
            actual_width = width - shadow_thickness + 1
        elif style == Table.PIECE_BAR or style == Table.PIECE_BORNE:
            width = self.inner_border_thickness * cf.PIECE_SIZE_PERCENTAGE
            shadow_thickness = width * cf.PIECE_SHADOW_THICKNESS
            actual_width = width - shadow_thickness + 1

        # Set coordinates.
        if style == Table.PIECE_NORMAL or style == Table.PIECE_GHOST:
            if style == Table.PIECE_NORMAL: i = len(target_pool)
            else: i = len(self.game_pieces[col])
            if 0 <= col <= 5 or 18 <= col <= 23:
                half = 0
            else: half = 1
            factor1 = col % 6
            factor2 = int(col / 12)
            if factor2 == 0: factor3 = 1
            else: factor3 = -1

            offset_x_pc = (self.offset_x['half'][half] +
                            self.temp_width['half'] * factor2 +
                            (self.temp_width['triangle'] / 2 +
                            self.temp_width['triangle'] * factor1) * factor3)

            offset_y_pc = (self.offset_y['half'][half] +
                            self.temp_height['half'] * factor2 +
                            (actual_width / 2 + actual_width * i) * factor3)
        elif style == Table.PIECE_BAR:
            if self.player_colors[self.board.get_player()] == color:
                factor = 1
                i = 1
            else:
                factor = -1
                i = 0
            j = len(target_pool)

            offset_x_pc = (self.offset_x['illusion'][1] -
                                self.inner_border_thickness * (i + 0.5))

            offset_y_pc = (self.offset_y['illusion'][0] +
                                self.temp_height['illusion'] * (1 - i) +
                                (actual_width / 2 + actual_width * j) * factor)
        elif style == Table.PIECE_BORNE:
            if self.player_colors[self.board.get_player()] == color: i = 0
            else: i = 1
            j = len(target_pool)

            offset_x_pc = (self.offset_x['label'][0] + self.temp_width['label']
                            + actual_width * (j + 1.5))

            offset_y_pc = (self.offset_y['global'] +
                                self.temp_height['illusion'] * i +
                                self.inner_border_thickness * (i + 0.5))

        # Draw piece.
        p = source_pool.pop()
        p.set_color(color)
        p.draw(offset_x_pc, offset_y_pc, width, selectable)
        target_pool.append(p)
        if aux_pool != None: aux_pool.append(p)


    def draw_canvas(self, init = False):
        if init:
            self.background = pm.Rect(0, 0, self.width, self.height, cf.BG_COLOR)
        else:
            self.background.draw(0, 0, self.width, self.height, cf.BG_COLOR)


    def draw_table_border(self, init = False):
        self.offset_x['global'] = (self.width - self.table_width) / 2
        self.offset_y['global'] = (self.height - self.table_height) / 2
        self.inner_border_thickness = (self.table_width *
                                            cf.INNER_BORDER_THICKNESS)
        gradient_end = (self.inner_border_thickness *
                                            cf.TABLE_BORDER_SHADOW_THICKNESS)

        if init:
            self.table_border = pm.Rect(self.offset_x['global'],
                                        self.offset_y['global'],
                                        self.table_width,
                                        self.table_height,
                                        cf.TABLE_BORDER_COLOR)

            self.table_border_shadow = gr.RectGradient(
                                self.offset_x['global'], self.offset_y['global'],
                                self.table_width, self.table_height,
                                cf.TABLE_BORDER_SHADOW_START_COLOR,
                                cf.TABLE_BORDER_SHADOW_END_COLOR,
                                0, gradient_end)

        else:
            self.table_border.draw(self.offset_x['global'],
                                    self.offset_y['global'],
                                    self.table_width,
                                    self.table_height,
                                    cf.TABLE_BORDER_COLOR)

            self.table_border_shadow.draw(
                                self.offset_x['global'], self.offset_y['global'],
                                self.table_width, self.table_height,
                                0, gradient_end)


    def draw_table_3d(self, init = False):
        self.temp_width['illusion'] = (self.table_width / 2 -
                                                self.inner_border_thickness * 2)
        self.temp_height['illusion'] = (self.table_height -
                                                self.inner_border_thickness * 2)
        self.inner_3d_thickness = self.table_width * cf.TABLE_INNER_3D_THICKNESS

        if init:
            self.halves_3d = []

        self.offset_x['illusion'] = []
        self.offset_y['illusion'] = []
        for i in range(2):
            self.offset_x['illusion'].append(self.offset_x['global'] +
                            self.temp_width['illusion'] * i +
                            self.inner_border_thickness * (2 * i + 1))
            self.offset_y['illusion'].append(self.offset_y['global'] +
                            self.inner_border_thickness)

            if init:
                self.halves_3d.append(gr.RectGradient(
                                self.offset_x['illusion'][i],
                                self.offset_y['illusion'][i],
                                self.temp_width['illusion'],
                                self.temp_height['illusion'],
                                cf.TABLE_INNER_3D_SHADOW_START_COLOR,
                                cf.TABLE_INNER_3D_SHADOW_END_COLOR,
                                0, self.inner_3d_thickness))
            else:
                self.halves_3d[i].draw(self.offset_x['illusion'][i],
                                self.offset_y['illusion'][i],
                                self.temp_width['illusion'],
                                self.temp_height['illusion'],
                                0, self.inner_3d_thickness)


    def draw_table_halves(self, init = False):
        thickness = self.inner_border_thickness + self.inner_3d_thickness
        self.temp_width['half'] = (self.temp_width['illusion'] -
                                                self.inner_3d_thickness * 2)
        self.temp_height['half'] = (self.temp_height['illusion'] -
                                                self.inner_3d_thickness * 2)
        if self.temp_width['half'] < self.temp_height['half']:
            gradient_end = (self.temp_width['half'] *
                                            cf.TABLE_HALF_BG_SHADOW_THICKNESS)
        else:
            gradient_end = (self.temp_height['half'] *
                                            cf.TABLE_HALF_BG_SHADOW_THICKNESS)

        if init:
            self.halves_bg = []
            self.halves_bg_shadow = []

        self.offset_x['half'] = []
        self.offset_y['half'] = []
        for i in range(2):
            self.offset_x['half'].append(self.offset_x['global'] +
                                            self.temp_width['half'] * i +
                                            thickness * (2 * i + 1))
            self.offset_y['half'].append(self.offset_y['global'] + thickness)

            if init:
                self.halves_bg.append(pm.Rect(self.offset_x['half'][i],
                                                self.offset_y['half'][i],
                                                self.temp_width['half'],
                                                self.temp_height['half'],
                                                cf.TABLE_HALF_BG_COLOR))

                self.halves_bg_shadow.append(gr.RectGradient(
                                self.offset_x['half'][i],
                                self.offset_y['half'][i],
                                self.temp_width['half'],
                                self.temp_height['half'],
                                cf.TABLE_HALF_BG_SHADOW_START_COLOR,
                                cf.TABLE_HALF_BG_SHADOW_END_COLOR,
                                0, gradient_end))
            else:
                self.halves_bg[i].draw(self.offset_x['half'][i],
                                        self.offset_y['half'][i],
                                        self.temp_width['half'],
                                        self.temp_height['half'],
                                        cf.TABLE_HALF_BG_COLOR)

                self.halves_bg_shadow[i].draw(
                                self.offset_x['half'][i],
                                self.offset_y['half'][i],
                                self.temp_width['half'],
                                self.temp_height['half'],
                                0, gradient_end)


    def draw_table_triangles(self, init = False):
        draw_color = 0
        colors = [cf.TABLE_TRIANGLE_BLACK_COLOR, cf.TABLE_TRIANGLE_RED_COLOR]
        self.temp_width['triangle'] = self.temp_width['half'] / 6
        triangle_spacing = self.temp_width['triangle'] * cf.TRIANGLE_SPACING
        self.temp_height['triangle'] = (self.temp_height['half'] *
                                                            cf.TRIANGLE_HEIGHT)
        triangle_pos = 1

        self.offset_x['tr_quarter'] = []
        self.offset_y['tr_quarter'] = []
        if init:
            self.triangles = []

        for i in range(2):
            offset_y_trh = i * self.temp_height['half']

            for j in range(2):
                self.offset_x['tr_quarter'].append(self.offset_x['half'][j])
                self.offset_y['tr_quarter'].append(self.offset_y['half'][j] +
                                                                offset_y_trh)

                for k in range(6):
                    vertex_array = [(self.offset_x['tr_quarter'][i*2 + j] +
                                        self.temp_width['triangle'] * k +
                                        triangle_spacing ,
                                        self.offset_y['tr_quarter'][i*2 + j]) ,

                                     (self.offset_x['tr_quarter'][i*2 + j] +
                                        self.temp_width['triangle'] * (k + 1) -
                                        triangle_spacing,
                                        self.offset_y['tr_quarter'][i*2 + j]) ,

                                     (self.offset_x['tr_quarter'][i*2 + j] +
                                        self.temp_width['triangle'] * (k + 0.5),
                                        self.offset_y['tr_quarter'][i*2 + j] +
                                        self.temp_height['triangle'] *
                                        triangle_pos)]

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
        self.temp_width['label'] = self.table_width * cf.HOME_LABEL_WIDTH
        self.temp_height['label'] = (self.inner_border_thickness *
                                    cf.HOME_LABEL_HEIGHT)

        corner_radius = self.temp_width['label'] * cf.HOME_LABEL_CORNER_RADIUS
        lb_text = [cf.HOME_LABEL_TEXT_PLAYER, cf.HOME_LABEL_TEXT_COMPUTER]

        self.offset_x['label'] = []
        self.offset_y['label'] = []
        if init:
            self.labels = []

        for i in range(2):
            self.offset_x['label'].append(self.offset_x['global'] +
                            self.table_width * cf.HOME_LABEL_SPACER)
            self.offset_y['label'].append(self.offset_y['global'] +
                            self.table_height * i - self.inner_border_thickness
                            * i + (self.inner_border_thickness -
                            self.temp_height['label']) / 2)

            if init:
                self.labels.append(pm.RoundedLabel(
                                self.offset_x['label'][i],
                                self.offset_y['label'][i],
                                self.temp_width['label'],
                                self.temp_height['label'], corner_radius,
                                cf.HOME_LABEL_BG_COLOR, lb_text[i],
                                cf.HOME_LABEL_TEXT_PROPORTION,
                                cf.HOME_LABEL_TEXT_FONT,
                                cf.HOME_LABEL_FG_COLOR))
            else:
                self.labels[i].draw(self.offset_x['label'][i],
                                    self.offset_y['label'][i],
                                    self.temp_width['label'],
                                    self.temp_height['label'], corner_radius,
                                    cf.HOME_LABEL_BG_COLOR, lb_text[i],
                                    cf.HOME_LABEL_TEXT_PROPORTION,
                                    cf.HOME_LABEL_TEXT_FONT,
                                    cf.HOME_LABEL_FG_COLOR)


    def draw_dices(self, init = False):
        self.temp_width['dice'] = (self.inner_border_thickness *
                                                    cf.DICE_SIZE_PERCENTAGE)
        corner_radius = self.temp_width['dice'] * cf.DICE_CORNER_RADIUS
        spacing = (self.inner_border_thickness - self.temp_width['dice']) / 2
        border = self.temp_width['dice'] * cf.DICE_SPACING_BORDER
        point_space_width = (self.temp_width['dice'] - border) / 3
        point_width = point_space_width * cf.DICE_POINT_WIDTH
        point_radius = point_width / 2

        if init:
            self.dices = []
            self.points = []

            for i in range(12):
                self.points.append(pm.Circle(0, 0, point_radius,
                                                            cf.DICE_FG_COLOR))
            self.active_points = []

        self.offset_x['dice'] = []
        self.offset_y['dice'] = []

        for point in self.active_points:
            self.points.append(point)
        self.active_points = []

        dices = self.board.get_dices()
        print dices

        for i in range(min(2, len(dices))):
            self.offset_x['dice'].append(self.offset_x['illusion'][0] +
                                            self.temp_width['illusion'] +
                                            self.inner_border_thickness * i +
                                            spacing)
            self.offset_y['dice'].append(self.offset_y['illusion'][0] +
                                            self.temp_height['illusion'] / 2 -
                                            self.inner_border_thickness +
                                            spacing)

            if init:
                self.dices.append(pm.RoundedRect(
                                    self.offset_x['dice'][i],
                                    self.offset_y['dice'][i],
                                    self.temp_width['dice'],
                                    self.temp_width['dice'], corner_radius,
                                    cf.DICE_BG_COLOR))
            else:
                self.dices[i].draw(self.offset_x['dice'][i],
                                    self.offset_y['dice'][i],
                                    self.temp_width['dice'],
                                    self.temp_width['dice'], corner_radius,
                                    cf.DICE_BG_COLOR)

            for j in range(dices[i]):
                point = self.points.pop()
                coords = self.dice_drawing[dices[i]][j]

                offset_x = (self.offset_x['dice'][i] + border / 2 +
                            point_space_width * (coords[0] + 0.5))
                offset_y = (self.offset_y['dice'][i] + border / 2 +
                            point_space_width * (coords[1] + 0.5))

                point.draw(offset_x, offset_y, point_radius, cf.DICE_FG_COLOR)
                self.active_points.append(point)

if __name__ == '__main__':
    "Please do not run this file directly, include it."
