import pyglet

import primitives as pm
import gradient as gr

import menu_graphic_config as cf
import button_graphic as btn


class Menu(object):
    offset_x = {}
    offset_y = {}
    temp_width = {}
    temp_height = {}

    def __init__(self, width, height, statistic):
        self.statistic = statistic

        self.draw(width, height, True)


    def mouse_motion(self, x, y, dx, dy):
        for button in self.main_buttons:
            if button.mouse_motion(x, y, dx, dy):
                return True

        return False


    def mouse_release_left(self, x, y):
        for button in self.main_buttons:
            button.mouse_release_left(x, y)


    def mouse_press_left(self, x, y):
        for button in self.main_buttons:
            button.mouse_press_left(x, y)


    def render(self):
        self.background.render()
        self.menu_border.render()
        self.content_bg.render()
        self.title.draw()
        self.subtitle.draw()
        for button in self.main_buttons:
            button.render()
        self.render_statistic()


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
        spacer = self.temp_height['content_bg'] * cf.BUTTON_MAIN_SPACER
        text = [cf.BUTTON_MAIN_TEXT_NEW, cf.BUTTON_MAIN_TEXT_RESET, cf.BUTTON_MAIN_TEXT_ABOUT, cf.BUTTON_MAIN_TEXT_EXIT]

        if init:
            self.main_buttons = []

        self.offset_x['button'] = []
        self.offset_y['button'] = []

        for i in range(len(text)):
            self.offset_x['button'].append(self.offset_x['content_bg'] + left_spacer)
            self.offset_y['button'].append(self.offset_y['content_bg'] + self.temp_height['content_bg'] - top_spacer - spacer * i - self.temp_height['button'] * i)

            if init:
                self.main_buttons.append(btn.Button(cf,
                                                    self.offset_x['button'][i],
                                                    self.offset_y['button'][i],
                                                    self.temp_width['button'],
                                                    self.temp_height['button'],
                                                    text[i]))
            else:
                self.main_buttons[i].draw(self.offset_x['button'][i],
                                            self.offset_y['button'][i],
                                            self.temp_width['button'],
                                            self.temp_height['button'])


    def render_statistic(self):
        self.statistic_title.draw()
        self.statistic_container.render()


    def draw_statistic(self, init = False):
        left_spacer = self.temp_width['content_bg'] * cf.STATISTIC_LEFT_SPACER
        top_spacer = self.temp_height['content_bg'] * cf.STATISTIC_TOP_SPACER
        self.offset_x['statistic'] = self.offset_x['content_bg'] + self.buttons_left_spacer + self.temp_width['button'] + left_spacer
        self.offset_y['statistic'] = self.offset_y['content_bg'] + self.temp_height['content_bg'] - top_spacer
        self.temp_width['statistic'] = self.temp_width['content_bg'] * cf.STATISTIC_WIDTH_PERCENTAGE
        self.temp_height['statistic'] = self.temp_height['content_bg'] * cf.STATISTIC_HEIGHT_PERCENTAGE

        title_height = self.temp_height['statistic'] * cf.STATISTIC_TITLE_HEIGHT_PERCENTAGE
        title_bottom_spacer = self.temp_height['statistic'] * cf.STATISTIC_TITLE_BOTTOM_SPACER
        title_left_spacer = self.temp_height['statistic'] * cf.STATISTIC_TITLE_LEFT_SPACER
        offset_x_title = self.offset_x['statistic'] + title_left_spacer
        offset_y_title = self.offset_y['statistic'] - title_height

        container_width = self.temp_width['statistic']
        container_height = self.temp_height['statistic'] - title_height - title_bottom_spacer
        offset_x_cont = self.offset_x['statistic']
        offset_y_cont = offset_y_title - title_bottom_spacer


        self.statistic_title = pyglet.text.Label(
                                    text = cf.STATISTIC_TITLE_TEXT,
                                    font_name = cf.STATISTIC_TITLE_FONT,
                                    font_size = title_height,
                                    color = cf.STATISTIC_TITLE_COLOR,
                                    x = offset_x_title, y = offset_y_title,
                                    anchor_x = 'left', anchor_y = 'bottom')

        if init:
            self.statistic_container = pm.Rect(offset_x_cont,
                                            offset_y_cont - container_height,
                                            container_width, container_height,
                                            cf.STATISTIC_CONTAINER_COLOR)
        else:
            self.statistic_container.draw(offset_x_cont,
                                            offset_y_cont - container_height,
                                            container_width, container_height,
                                            cf.STATISTIC_CONTAINER_COLOR)


if __name__ == '__main__':
    "Please do not run this file directly, include it."
