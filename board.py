import random

class Board: 
     
    allSpaces = []   
    dices = []
    
    computer = 'computer'
    player = 'player'
    empty = 'nobody'
    
    def __init__(self):
        for i in range(25):
            self.allSpaces.insert(i, (0, self.empty)) # n = nothing
            
        self.allSpaces[0] = (0, self.computer, 0, self.player) # bar
        self.allSpaces[1] = (2, self.computer) # c = computer, p = player
        self.allSpaces[6] = (5, self.player)
        self.allSpaces[8] = (3, self.player)
        self.allSpaces[12] = (5, self.computer)
        self.allSpaces[13] = (5, self.player)
        self.allSpaces[17] = (3, self.computer)
        self.allSpaces[19] = (5, self.computer)
        self.allSpaces[24] = (2, self.player)
        
        for i in range(25) :
            self.allSpaces[i] = list(self.allSpaces[i])
            
        return
    
    def generate_dices(self):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6) 

        if (dice1 == dice2) :
            self.dices = [dice1, dice1, dice1, dice1]
        else:
            self.dices = [dice1, dice2]
        
        return self.dices 
    
    def get_dices(self):
        return self.dices    
    
    def printb(self):
        for i in range(25): 
            print i, " ", self.allSpaces[i] 
    
    
    def valid_player_move(self, col, n) :
        bar = self.allSpaces[0]
        if (bar[2] != 0 and col != 0) :
            print "Invalid move - you have pieces on the bar"
            return False
        else:
            if (col == 0) :
                destination = self.allSpaces[25 - n]
            else :
                destination = self.allSpaces[col - n]
            if (destination[1] == self.computer and destination[0] > 1) :
                print "Invalid move - destination occupied"
                return False
        return True
    

    def move_player(self, col, n) :
        if (self.valid_player_move(col, n) == False) :
            print "Can't do the move"
            return False
        else:
            self.dices.remove(n)
            if (col == 0) :
                bar = self.allSpaces[0]
                bar[2] -= 1
                destination = self.allSpaces[25-n]
            else :
                source = self.allSpaces[col]
                source[0] -= 1
                if (source[0] == 0) :
                    source[1] = self.empty
                destination = self.allSpaces[col - n]
            if (destination[1] == self.computer and destination[0] == 1) :
                destination[1] = self.player
                bar[0] += 1
            else :
                destination[0] += 1
                destination[1] = self.player
        return True

    def get_player_destinations(self, col):
        dest = [] # 25 = you can move it out 

        if (self.allSpaces[col][1] == self.player or
            (col == 0 and self.allSpaces[col][2] != 0)) :
            if (col == 0) :
                for i in range(2):
                    if (self.allSpaces[25 - self.dices[i]][1] == self.player or
                        self.allSpaces[25 - self.dices[i]][1] == self.empty or 
                        (self.allSpaces[25 - self.dices[i]][1] == self.computer and 
                         self.allSpaces[25 - self.dices[i]][0] == 1)) :
                        dest.append(25 - self.dices[i])
            else :
                t = True
                for i in range (7, 25) :
                    if (self.allSpaces[i][1] == self.player) :
                        t = False
                        break
                if (t == False) :
                    for i in range(len(self.dices)):
                        if (col - self.dices[i] >= 1) :
                            if (self.allSpaces[col - self.dices[i]][1] == self.player or
                                self.allSpaces[col - self.dices[i]][1] == self.empty or
                                (self.allSpaces[col - self.dices[i]][1] == self.computer and
                                 self.allSpaces[col - self.dices[i]][0] == 1)) :
                                dest.append(col - self.dices[i])
                else:
                    for i in range(len(self.dices)):
                        if (col - self.dices[i] >= 1) :
                            if (self.allSpaces[col - self.dices[i]][1] == self.player or
                                self.allSpaces[col - self.dices[i]][1] == self.empty or
                                (self.allSpaces[col - self.dices[i]][1] == self.computer and 
                                 self.allSpaces[col - self.dices[i]][0] == 1)) : 
                                dest.append(col - self.dices[i])
                        else :
                            dest.append(25)
            return dest
        else:
            print "Invalid! You don't have any piece here"
            return dest

    def get_spaces(self):
        return self.allSpaces

    def get_player(self):
        return self.player

    def get_computer(self):
        return self.computer
