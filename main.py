import pyglet
from pyglet.gl import *
import primitives


class BackgammonWindow(pyglet.window.Window):
    RELATIVE_WIDTH = 1000
    RELATIVE_HEIGHT = 600
    BORDER_THICKNESS = 15
    INNER_BORDER_THICKNESS = 18
    INNER_3D_THICKNESS = 8
    BG_COLOR = (0.9, 0.9, 0.9, 1)
    TABLE_BG_COLOR = (0.6, 0.5, 0.3, 1)
    TABLE_HALF_BG_COLOR = (0.7, 0.6, 0.4, 1)
    TABLE_HALF_3D_COLOR = (0.5, 0.4, 0.2, 1)

    def __init__(self, config):
        super(BackgammonWindow, self).__init__(resizable=True, config=config)
        self.set_minimum_size(self.RELATIVE_WIDTH/2, self.RELATIVE_HEIGHT/2)
        self.set_size(self.RELATIVE_WIDTH + self.BORDER_THICKNESS * 2,
                      self.RELATIVE_HEIGHT + self.BORDER_THICKNESS * 2)
        self.set_caption('Backgammon')

        self.label = pyglet.text.Label('Backgammon test',
                          font_name='Arial',
                          font_size=24,
                          x=self.width//2, y=self.height//2,
                          anchor_x='center', anchor_y='center')

        self.draw_table(True)

    def on_draw(self):
        self.clear()
        self.render_table()
        self.label.draw()

    def on_resize(self, width, height):
        super(BackgammonWindow, self).on_resize(width, height)
        self.label.x = width//2
        self.label.y = height//2

        self.draw_table()

    def resize_table(self):
        temp_width = self.width
        temp_height = temp_width * self.RELATIVE_HEIGHT / self.RELATIVE_WIDTH
        if temp_height > self.height:
            temp_height = self.height
            temp_width = temp_height * self.RELATIVE_WIDTH / self.RELATIVE_HEIGHT

        self.table_width = temp_width - self.BORDER_THICKNESS * 2
        self.table_height = temp_height - self.BORDER_THICKNESS * 2

    def render_table(self):
        self.background.render()
        self.table_bg.render()
        for half_3d in self.halves_3d:
            half_3d.render()
        for half_bg in self.halves_bg:
            half_bg.render()


    def draw_table(self, init = False):
        self.resize_table()

        # Draw neutral background.
        vertex_array = [(0, 0),
                        (self.width, 0),
                        (self.width, self.height),
                        (0, self.height)]
        if init:
            self.background = primitives.Polygon(v = vertex_array,
                                        color = self.BG_COLOR, style = 0)
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
                                                color = self.TABLE_BG_COLOR)
        else:
            self.table_bg.v = vertex_array

        # Draw table 3D illusion.
        temp_width = self.table_width / 2 - self.INNER_BORDER_THICKNESS * 2
        temp_height = self.table_height - self.INNER_BORDER_THICKNESS * 2

        if init:
            self.halves_3d = []

        for i in range(2):
            offset_x = gl_offset_x + temp_width * i + self.INNER_BORDER_THICKNESS * (2 * i + 1)
            offset_y = gl_offset_y + self.INNER_BORDER_THICKNESS
            vertex_array = [(offset_x, offset_y),
                            (offset_x + temp_width, offset_y),
                            (offset_x + temp_width, offset_y + temp_height),
                            (offset_x, offset_y + temp_height)]

            if init:
                self.halves_3d.append(primitives.Polygon(v = vertex_array,
                                                    color = self.TABLE_HALF_3D_COLOR))
            else:
                self.halves_3d[i].v = vertex_array


        # Draw table halves backgrounds.
        temp_width = temp_width - self.INNER_3D_THICKNESS * 2
        temp_height = temp_height - self.INNER_3D_THICKNESS * 2

        if init:
            self.halves_bg = []

        for i in range(2):
            offset_x = gl_offset_x + temp_width * i + (self.INNER_BORDER_THICKNESS + self.INNER_3D_THICKNESS) * (2 * i + 1)
            offset_y = gl_offset_y + self.INNER_BORDER_THICKNESS + self.INNER_3D_THICKNESS 
            vertex_array = [(offset_x, offset_y),
                            (offset_x + temp_width, offset_y),
                            (offset_x + temp_width, offset_y + temp_height),
                            (offset_x, offset_y + temp_height)]

            if init:
                self.halves_bg.append(primitives.Polygon(v = vertex_array,
                                                    color = self.TABLE_HALF_BG_COLOR))
            else:
                self.halves_bg[i].v = vertex_array

        # TODO: Draw triangles

if __name__ == '__main__':
    try:
        config = Config(sample_buffers=1, samples=4, depth_size=16,
                        double_buffer=True)
    except pyglet.window.NoSuchConfigException:
        print "Smooth contex could not be aquiried."
        config = None

    window = BackgammonWindow(config)
    pyglet.app.run()
