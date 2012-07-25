import json
import os

class Statistic(object):
    FILE = './statistic.dat'
    LEVELS = 3
    LEVEL1 = 'easy'
    LEVEL2 = 'normal'
    LEVEL3 = 'hard'
    GAME_NR = 'games'
    WINS = 'wins'
    LOSSES = 'losses'

    def __init__(self, file = FILE):
        self.FILE = file
        if not os.path.isfile(self.FILE):
            self.reset()
            self.save()

        f = open(self.FILE, 'r')
        self.data = json.load(f)
        f.close()


    def reset(self):
        self.data = {Statistic.LEVEL1 :
                        {Statistic.GAME_NR : 0,
                         Statistic.WINS : 0,
                         Statistic.LOSSES : 0},
                     Statistic.LEVEL2 :
                        {Statistic.GAME_NR : 0,
                         Statistic.WINS : 0,
                         Statistic.LOSSES : 0},
                     Statistic.LEVEL3 :
                        {Statistic.GAME_NR : 0,
                         Statistic.WINS : 0,
                         Statistic.LOSSES : 0}}
        self.save()


    def save(self):
        f = open(self.FILE, 'w')
        json.dump(self.data, f)
        f.close()


    def get_data(self, level, prop):
        return self.data[level][prop]


