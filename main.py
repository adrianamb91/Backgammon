import pyglet
from pyglet.gl import *
import primitives
import backgammon_config as conf
import table_graphic


class BackgammonWindow(pyglet.window.Window):
    def __init__(self, config):
        super(BackgammonWindow, self).__init__(resizable=True, config=config)
        self.set_minimum_size(conf.RELATIVE_WIDTH/2, conf.RELATIVE_HEIGHT/2)
        self.set_size(conf.RELATIVE_WIDTH + conf.BORDER_THICKNESS * 2,
                      conf.RELATIVE_HEIGHT + conf.BORDER_THICKNESS * 2)
        self.set_caption('Backgammon')

        self.GAME_TABLE = table_graphic.Table(self.width, self.height)
        #self.MENU = menu_graphic.Menu()

        self.CURRENT_SCREEN = self.GAME_TABLE

    def on_draw(self):
        self.clear()
        self.CURRENT_SCREEN.render()

    def on_resize(self, width, height):
        super(BackgammonWindow, self).on_resize(width, height)
        self.CURRENT_SCREEN.draw(w = width, h = height)

if __name__ == '__main__':
    try:
        config = Config(alpha_size = 8, sample_buffers = 1, samples = 4,
                        depth_size = 0, double_buffer = True)
        window = BackgammonWindow(config)
    except pyglet.window.NoSuchConfigException:
        print "Smooth contex could not be aquired."
        window = BackgammonWindow(None)
        
    pyglet.app.run()
