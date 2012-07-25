import pyglet

import primitives as pm
import gradient as gr

import menu_graphic_config as cf
import button_graphic as btn
import statistic as st


class Menu(object):
    offset_x = {}
    offset_y = {}
    temp_width = {}
    temp_height = {}

    ACTION_NEW_GAME = 0
    ACTION_RESET_STATS = 1
    ACTION_ABOUT = 2
    ACTION_EXIT = 3

    DIALOG_NEW_GAME = 0
    DIALOG_ABOUT = 1

    current_dialog = None

    def __init__(self, width, height, statistic):
        self.statistic = statistic

        self.draw(width, height, True)


    def mouse_motion(self, x, y, dx, dy):
        if self.current_dialog == None:
            for button in self.main_buttons:
                if button[0].mouse_motion(x, y, dx, dy):
                    return True
        else:
            if self.dialog_close.mouse_motion(x, y, dx, dy):
                return True

        return False


    def mouse_release_left(self, x, y):
        if self.current_dialog == None:
            for button in self.main_buttons:
                if button[0].mouse_release_left(x, y):
                    if button[1] == Menu.ACTION_NEW_GAME:
                        self.draw_dialog(Menu.DIALOG_NEW_GAME, True)
                    elif button[1] == Menu.ACTION_RESET_STATS:
                        self.statistic.reset()
                        self.draw_statistic()
                    elif button[1] == Menu.ACTION_ABOUT:
                        self.draw_dialog(Menu.DIALOG_ABOUT, True)
                    elif button[1] == Menu.ACTION_EXIT:
                        return True
        else:
            if self.dialog_close.mouse_release_left(x, y):
                self.current_dialog = None
                self.render()
        return False


    def mouse_press_left(self, x, y):
        if self.current_dialog == None:
            for button in self.main_buttons:
                button[0].mouse_press_left(x, y)
        else:
            self.dialog_close.mouse_press_left(x, y)


    def render(self):
        self.background.render()
        self.menu_border.render()
        self.content_bg.render()
        self.title.draw()
        self.subtitle.draw()
        for button in self.main_buttons:
            button[0].render()
        self.render_statistic()
        self.render_dialog()


    def draw(self, w, h, init = False):
        self.width = w
        self.height = h
        self.resize()

        self.draw_canvas(init)
        self.draw_border(init)
        self.draw_content_bg(init)
        self.draw_title(init)
        self.draw_buttons(init)
        self.draw_statistic(init)

        self.draw_dialog(self.current_dialog)


    def resize(self):
        temp_width = self.width - cf.BORDER_THICKNESS * 2
        temp_height = temp_width * cf.RELATIVE_HEIGHT / cf.RELATIVE_WIDTH
        if temp_height > self.height:
            temp_height = self.height - cf.BORDER_THICKNESS * 2
            temp_width = temp_height * cf.RELATIVE_WIDTH / cf.RELATIVE_HEIGHT

        self.menu_width = temp_width
        self.menu_height = temp_height


    def draw_canvas(self, init = False):
        if init:
            self.background = pm.Rect(0, 0, self.width, self.height, cf.BG_COLOR)
        else:
            self.background.draw(0, 0, self.width, self.height, cf.BG_COLOR)


    def draw_border(self, init = False):
        self.offset_x['global'] = (self.width - self.menu_width) / 2
        self.offset_y['global'] = (self.height - self.menu_height) / 2
        self.global_border_width = (self.menu_width * cf.MENU_BORDER_THICKNESS)

        if init:
            self.menu_border = pm.Rect(self.offset_x['global'],
                                        self.offset_y['global'],
                                        self.menu_width,
                                        self.menu_height,
                                        cf.MENU_BORDER_COLOR)
        else:
            self.menu_border.draw(self.offset_x['global'],
                                    self.offset_y['global'],
                                    self.menu_width,
                                    self.menu_height,
                                    cf.MENU_BORDER_COLOR)

    def draw_content_bg(self, init = False):
        self.offset_x['content_bg'] = (self.offset_x['global'] + self.global_border_width)
        self.offset_y['content_bg'] = (self.offset_y['global'] + self.global_border_width)
        self.temp_width['content_bg'] = self.menu_width - self.global_border_width * 2
        self.temp_height['content_bg'] = self.menu_height - self.global_border_width * 2

        if init:
            self.content_bg = gr.BandGradient(self.offset_x['content_bg'],
                                                self.offset_y['content_bg'],
                                                self.temp_width['content_bg'],
                                                self.temp_height['content_bg'],
                                                cf.MENU_BG_START_COLOR,
                                                cf.MENU_BG_END_COLOR)
        else:
            self.content_bg.draw(self.offset_x['content_bg'],
                                    self.offset_y['content_bg'],
                                    self.temp_width['content_bg'],
                                    self.temp_height['content_bg'])

    def draw_title(self, init = False):
        self.offset_x['title'] = (self.width / 2)
        self.offset_y['title'] = (self.offset_y['content_bg'] + self.temp_height['content_bg'] * (1 - cf.TITLE_TOP_SPACER))
        title_size = self.temp_height['content_bg'] * cf.TITLE_PROPORTION

        self.offset_x['subtitle'] = (self.width / 2 + self.temp_width['content_bg'] * cf.SUBTITLE_OFFSET)
        self.offset_y['subtitle'] = (self.offset_y['title'] - title_size - self.temp_height['content_bg'] * cf.SUBTITLE_TOP_SPACER)
        subtitle_size = self.temp_height['content_bg'] * cf.SUBTITLE_PROPORTION

        self.title = pyglet.text.Label(cf.TITLE_TEXT, font_name = cf.TITLE_FONT,
                                        font_size = title_size, bold = True,
                                        color = cf.TITLE_COLOR,
                                        x = self.offset_x['title'],
                                        y = self.offset_y['title'],
                                        anchor_x = 'center', anchor_y = 'top')

        self.subtitle = pyglet.text.Label(cf.SUBTITLE_TEXT, font_name = cf.SUBTITLE_FONT,
                                        font_size = subtitle_size, bold = True,
                                        color = cf.SUBTITLE_COLOR,
                                        x = self.offset_x['subtitle'],
                                        y = self.offset_y['subtitle'],
                                        anchor_x = 'center', anchor_y = 'top')

    def draw_buttons(self, init = False):
        self.temp_width['button'] = self.temp_width['content_bg'] * cf.BUTTON_MAIN_WIDTH
        self.temp_height['button'] = self.temp_height['content_bg'] * cf.BUTTON_MAIN_HEIGHT
        top_spacer = self.temp_height['content_bg'] * cf.BUTTON_MAIN_TOP_SPACER
        left_spacer = self.temp_width['content_bg'] * cf.BUTTON_MAIN_LEFT_SPACER
        self.buttons_left_spacer = left_spacer
        spacer_horizontal = self.temp_width['content_bg'] * cf.BUTTON_MAIN_HORIZONTAL_SPACER
        spacer_vertical = self.temp_height['content_bg'] * cf.BUTTON_MAIN_VERTICAL_SPACER
        text = [cf.BUTTON_MAIN_TEXT_NEW, cf.BUTTON_MAIN_TEXT_RESET, cf.BUTTON_MAIN_TEXT_ABOUT, cf.BUTTON_MAIN_TEXT_EXIT]
        action = [Menu.ACTION_NEW_GAME, Menu.ACTION_RESET_STATS, Menu.ACTION_ABOUT, Menu.ACTION_EXIT]

        if init:
            self.main_buttons = []

        self.offset_x['button'] = []
        self.offset_y['button'] = []

        for i in range(len(text)):
            self.offset_x['button'].append(self.offset_x['content_bg'] + left_spacer + self.temp_width['button'] * (i % 2) + spacer_horizontal * (i % 2))
            self.offset_y['button'].append(self.offset_y['content_bg'] + self.temp_height['content_bg'] - top_spacer - (self.temp_height['button'] + spacer_vertical) * (int(i / 2)))

            if init:
                self.main_buttons.append([btn.Button(cf,
                                                    self.offset_x['button'][i],
                                                    self.offset_y['button'][i],
                                                    self.temp_width['button'],
                                                    self.temp_height['button'],
                                                    text[i]),
                                            action[i]])
            else:
                self.main_buttons[i][0].draw(self.offset_x['button'][i],
                                                self.offset_y['button'][i],
                                                self.temp_width['button'],
                                                self.temp_height['button'])


    def render_statistic(self):
        self.statistic_container.render()
        self.statistic_title.draw()
        for header in self.statistic_vertical_headers:
            header.render()
        for label in self.statistic_vertical_header_labels:
            label.draw()
        for header in self.statistic_horizontal_headers:
            header.render()
        for label in self.statistic_horizontal_header_labels:
            label.draw()
        for labels in self.statistic_labels:
            for label in labels:
                label.draw()


    def draw_statistic(self, init = False):
        left_spacer = self.temp_width['content_bg'] * cf.STATISTIC_LEFT_SPACER
        top_spacer = self.temp_height['content_bg'] * cf.STATISTIC_TOP_SPACER
        self.offset_x['statistic'] = self.offset_x['content_bg'] + left_spacer
        self.offset_y['statistic'] = self.offset_y['content_bg'] + self.temp_height['content_bg'] - top_spacer
        self.temp_width['statistic'] = self.temp_width['content_bg'] * cf.STATISTIC_WIDTH_PERCENTAGE
        self.temp_height['statistic'] = self.temp_height['content_bg'] * cf.STATISTIC_HEIGHT_PERCENTAGE

        header_width = self.temp_width['statistic'] * cf.STATISTIC_HEADER_WIDTH_PERCENTAGE
        header_height = self.temp_height['statistic'] * cf.STATISTIC_HEADER_HEIGHT_PERCENTAGE
        cell_width = (self.temp_width['statistic'] - header_width) / 3
        cell_height = (self.temp_height['statistic'] - header_height) / self.statistic.LEVELS
        tx_size = header_height * cf.STATISTIC_TEXT_PERCENTAGE
        border = cf.STATISTIC_TABLE_BORDER

        properties = [[cf.STATISTIC_PROPERTY_GAMES_NR, self.statistic.GAME_NR],
                        [cf.STATISTIC_PROPERTY_WINS, self.statistic.WINS],
                        [cf.STATISTIC_PROPERTY_LOSSES, self.statistic.LOSSES]]
        levels = [[cf.STATISTIC_LEVEL1, self.statistic.LEVEL1],
                    [cf.STATISTIC_LEVEL2, self.statistic.LEVEL2],
                    [cf.STATISTIC_LEVEL3, self.statistic.LEVEL3]]


        if init:
            self.statistic_container = pm.Rect(self.offset_x['statistic'],
                                            self.offset_y['statistic'] - self.temp_height['statistic'],
                                            self.temp_width['statistic'], self.temp_height['statistic'],
                                            cf.STATISTIC_CONTAINER_COLOR)
        else:
            self.statistic_container.draw(self.offset_x['statistic'],
                                            self.offset_y['statistic'] - self.temp_height['statistic'],
                                            self.temp_width['statistic'], self.temp_height['statistic'],
                                            cf.STATISTIC_CONTAINER_COLOR)

        self.statistic_title = pyglet.text.Label(
                                    text = cf.STATISTIC_TITLE_TEXT,
                                    font_name = cf.STATISTIC_TITLE_FONT,
                                    font_size = tx_size,
                                    color = cf.STATISTIC_TITLE_COLOR,
                                    x = self.offset_x['statistic'] + header_width / 2,
                                    y = self.offset_y['statistic'] - header_height / 2,
                                    anchor_x = 'center', anchor_y = 'center')

        if init:
            self.statistic_vertical_headers = []
            self.statistic_vertical_header_labels = []

        offset_x_header = self.offset_x['statistic'] + header_width
        offset_y_header = self.offset_y['statistic'] - header_height
        offset_y_text = offset_y_header + header_height / 2
        for i in range(3):
            offset_x_cell = offset_x_header + cell_width * i
            offset_x_text = offset_x_cell + cell_width / 2

            if init:
                self.statistic_vertical_headers.append(pm.Rect(
                                    offset_x_cell + border, offset_y_header + border,
                                    cell_width - border * 2, header_height - border * 2,
                                    cf.STATISTIC_HEADER_BG_COLOR))
                self.statistic_vertical_header_labels.append(
                                pyglet.text.Label(
                                    text = properties[i][0],
                                    font_name = cf.STATISTIC_TABLE_FONT,
                                    font_size = tx_size,
                                    color = cf.STATISTIC_HEADER_FG_COLOR,
                                    x = offset_x_text, y = offset_y_text,
                                    anchor_x = 'center', anchor_y = 'center'))
            else:
                self.statistic_vertical_headers[i].draw(
                                    offset_x_cell + border, offset_y_header + border,
                                    cell_width - border * 2, header_height - border * 2,
                                    cf.STATISTIC_HEADER_BG_COLOR)
                self.statistic_vertical_header_labels[i] = pyglet.text.Label(
                                    text = properties[i][0],
                                    font_name = cf.STATISTIC_TABLE_FONT,
                                    font_size = tx_size,
                                    color = cf.STATISTIC_HEADER_FG_COLOR,
                                    x = offset_x_text, y = offset_y_text,
                                    anchor_x = 'center', anchor_y = 'center')

        if init:
            self.statistic_horizontal_headers = []
            self.statistic_horizontal_header_labels = []

        offset_x_header = self.offset_x['statistic']
        offset_y_header = self.offset_y['statistic'] - header_height - cell_height
        offset_x_text = offset_x_header + header_width / 2
        for i in range(self.statistic.LEVELS):
            offset_y_cell = offset_y_header - cell_height * i
            offset_y_text = offset_y_cell + cell_height / 2

            if init:
                self.statistic_horizontal_headers.append(pm.Rect(
                                    offset_x_header + border, offset_y_cell + border,
                                    header_width - border * 2, cell_height - border * 2,
                                    cf.STATISTIC_HEADER_BG_COLOR))
                self.statistic_horizontal_header_labels.append(
                                pyglet.text.Label(
                                    text = levels[i][0],
                                    font_name = cf.STATISTIC_TABLE_FONT,
                                    font_size = tx_size,
                                    color = cf.STATISTIC_HEADER_FG_COLOR,
                                    x = offset_x_text, y = offset_y_text,
                                    anchor_x = 'center', anchor_y = 'center'))
            else:
                self.statistic_horizontal_headers[i].draw(
                                    offset_x_header + border, offset_y_cell + border,
                                    header_width - border * 2, cell_height - border * 2,
                                    cf.STATISTIC_HEADER_BG_COLOR)
                self.statistic_horizontal_header_labels[i] = pyglet.text.Label(
                                    text = levels[i][0],
                                    font_name = cf.STATISTIC_TABLE_FONT,
                                    font_size = tx_size,
                                    color = cf.STATISTIC_HEADER_FG_COLOR,
                                    x = offset_x_text, y = offset_y_text,
                                    anchor_x = 'center', anchor_y = 'center')

        if init:
            self.statistic_labels = []

        offset_x_row = self.offset_x['statistic'] + header_width
        for i in range(self.statistic.LEVELS):
            offset_y_row = self.offset_y['statistic'] - header_height - cell_height * (i + 0.5)
            if init:
                self.statistic_labels.append([])

            for j in range(3):
                offset_x_cell = offset_x_row + cell_width * (j + 0.5)

                if init:
                    self.statistic_labels[i].append(
                                pyglet.text.Label(
                                    text = str(self.statistic.get_data(levels[i][1], properties[j][1])),
                                    font_name = cf.STATISTIC_TABLE_FONT,
                                    font_size = tx_size,
                                    color = cf.STATISTIC_FG_COLOR,
                                    x = offset_x_cell, y = offset_y_row,
                                    anchor_x = 'center', anchor_y = 'center'))
                else:
                    self.statistic_labels[i][j] = pyglet.text.Label(
                                    text = str(self.statistic.get_data(levels[i][1], properties[j][1])),
                                    font_name = cf.STATISTIC_TABLE_FONT,
                                    font_size = tx_size,
                                    color = cf.STATISTIC_FG_COLOR,
                                    x = offset_x_cell, y = offset_y_row,
                                    anchor_x = 'center', anchor_y = 'center')


    def render_dialog(self):
        if self.current_dialog != None:
            self.dialog_outer.render()
            self.dialog_inner.render()
            self.dialog_title.draw()
            self.dialog_close.render()


    def draw_dialog(self, style, init = False):
        if init:
            self.current_dialog = style

        if self.current_dialog != None:
            self.temp_width['dialog'] = self.menu_width * cf.DIALOG_WIDTH_PERCENTAGE
            self.temp_height['dialog'] = self.menu_height * cf.DIALOG_HEIGHT_PERCENTAGE

            self.offset_x['dialog'] = self.offset_x['global'] + (self.menu_width - self.temp_width['dialog']) / 2
            self.offset_y['dialog'] = self.offset_y['global'] + (self.menu_height - self.temp_height['dialog']) / 2

            self.temp_width['inner_dialog'] = self.temp_width['dialog'] - cf.DIALOG_BORDER_THICKNESS * 2
            self.temp_height['inner_dialog'] = self.temp_height['dialog'] - cf.DIALOG_BORDER_THICKNESS * 2

            self.offset_x['inner_dialog'] = self.offset_x['dialog'] + cf.DIALOG_BORDER_THICKNESS
            self.offset_y['inner_dialog'] = self.offset_y['dialog'] + cf.DIALOG_BORDER_THICKNESS

            title_spacer = self.temp_height['inner_dialog'] * cf.DIALOG_TITLE_TOP_SPACER
            tx_size = self.temp_height['inner_dialog'] * cf.DIALOG_TITLE_PERCENTAGE
            if style == Menu.DIALOG_NEW_GAME: text = cf.DIALOG_TITLE_NEW_GAME
            elif style == Menu.DIALOG_ABOUT: text = cf.DIALOG_TITLE_ABOUT
            self.offset_x['dialog_title'] = self.offset_x['inner_dialog'] + self.temp_width['inner_dialog'] / 2
            self.offset_y['dialog_title'] = self.offset_y['inner_dialog'] + self.temp_height['inner_dialog'] - title_spacer

            self.temp_width['dialog_close'] = self.temp_width['inner_dialog'] * cf.DIALOG_BUTTON_WIDTH_PERCENTAGE
            self.temp_height['dialog_close'] = self.temp_height['inner_dialog'] * cf.DIALOG_BUTTON_HEIGHT_PERCENTAGE
            close_button_spacer = self.temp_height['inner_dialog'] * cf.DIALOG_CLOSE_BUTTON_SPACER
            self.offset_x['dialog_close'] = self.offset_x['inner_dialog'] + (self.temp_width['inner_dialog'] - self.temp_width['dialog_close']) / 2
            self.offset_y['dialog_close'] = self.offset_y['inner_dialog'] + close_button_spacer

            if init:
                self.dialog_outer = pm.Rect(self.offset_x['dialog'],
                                            self.offset_y['dialog'],
                                            self.temp_width['dialog'],
                                            self.temp_height['dialog'],
                                            cf.DIALOG_BORDER_COLOR)
                self.dialog_inner = pm.Rect(self.offset_x['inner_dialog'],
                                            self.offset_y['inner_dialog'],
                                            self.temp_width['inner_dialog'],
                                            self.temp_height['inner_dialog'],
                                            cf.DIALOG_BG_COLOR)
                self.dialog_close = btn.Button(cf,
                                                self.offset_x['dialog_close'],
                                                self.offset_y['dialog_close'],
                                                self.temp_width['dialog_close'],
                                                self.temp_height['dialog_close'],
                                                cf.DIALOG_CLOSE_BUTTON_TEXT)
            else:
                self.dialog_outer.draw(self.offset_x['dialog'],
                                        self.offset_y['dialog'],
                                        self.temp_width['dialog'],
                                        self.temp_height['dialog'],
                                        cf.DIALOG_BORDER_COLOR)
                self.dialog_inner.draw(self.offset_x['inner_dialog'],
                                        self.offset_y['inner_dialog'],
                                        self.temp_width['inner_dialog'],
                                        self.temp_height['inner_dialog'],
                                        cf.DIALOG_BG_COLOR)
                self.dialog_close.draw(self.offset_x['dialog_close'],
                                        self.offset_y['dialog_close'],
                                        self.temp_width['dialog_close'],
                                        self.temp_height['dialog_close'])

            self.dialog_title = pyglet.text.Label(text = text,
                                            font_name = cf.DIALOG_TITLE_FONT,
                                            font_size = tx_size,
                                            color = cf.DIALOG_TITLE_COLOR,
                                            x = self.offset_x['dialog_title'],
                                            y = self.offset_y['dialog_title'],
                                            anchor_x = 'center',
                                            anchor_y = 'top')



















if __name__ == '__main__':
    "Please do not run this file directly, include it."
