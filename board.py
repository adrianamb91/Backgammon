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

    def get_spaces(self):
        return self.allSpaces

    def get_player(self):
        return self.player

    def get_computer(self):
        return self.computer
