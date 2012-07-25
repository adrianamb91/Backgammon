import json
import os

class Statistic(object):
    FILE = './statistic.dat'

    def __init__(self, file = FILE):
        self.FILE = file
        if not os.path.isfile(self.FILE):
            self.reset()
            self.save()

        f = open(self.FILE, 'r')
        self.data = json.load(f)
        f.close()


    def reset(self):
        self.data = {   'easy'   : {'games' : 0, 'winp' : 0, 'lossp' : 0},
                        'normal' : {'games' : 0, 'winp' : 0, 'lossp' : 0},
                        'hard'   : {'games' : 0, 'winp' : 0, 'lossp' : 0}}
        self.save()


    def save(self):
        f = open(self.FILE, 'w')
        json.dump(self.data, f)
        f.close()


    def get_data(self):
        return self.data
