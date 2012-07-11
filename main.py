import pyglet
from pyglet.gl import *


class BackgammonWindow(pyglet.window.Window):
    def __init__(self, config):
        super(BackgammonWindow, self).__init__(resizable=True, config=config)
        self.set_caption('Backgammon')

        self.label = pyglet.text.Label('Backgammon test',
                          font_name='Arial',
                          font_size=24,
                          x=self.width//2, y=self.height//2,
                          anchor_x='center', anchor_y='center')

    def on_draw(self):
        self.clear()
        self.label.draw()

    def on_resize(self, width, height):
        super(BackgammonWindow, self).on_resize(width, height)
        self.label.x = width//2
        self.label.y = height//2

if __name__ == '__main__':
    try:
        config = Config(sample_buffers=1, samples=4, depth_size=16,
                        double_buffer=True)
    except pyglet.window.NoSuchConfigException:
        print "Smooth contex could not be aquiried."
        config = None

    window = BackgammonWindow(config)
    pyglet.app.run()
