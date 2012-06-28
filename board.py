class Board:  
    allSpaces = []
    def __init__(self):
        for i in range(25):
            self.allSpaces.insert(i, (0, 'n')) # n = nothing
            
        self.allSpaces[0] = (0, 'c', 0, 'p')
        self.allSpaces[1] = (2, 'c') # c = computer, p = player
        self.allSpaces[6] = (5, 'p')
        self.allSpaces[8] = (3, 'p')
        self.allSpaces[12] = (5, 'c')
        self.allSpaces[13] = (5, 'p')
        self.allSpaces[17] = (3, 'c')
        self.allSpaces[19] = (5, 'c')
        self.allSpaces[24] = (2, 'p')
        
        for i in range(25) :
            self.allSpaces[i] = list(self.allSpaces[i])
            
            
    def make_computer_move(self, col, n) :
        source = self.allSpaces[col]
        if (col > 0 and (source[0] == 0 or 'c' != source[1])) :
            print "Invalid move - invalid source"
            return -1
        elif (col+n < 0) :
            print "Invalid move - invalid destination"
            return -1
        else:
            destination = self.allSpaces[col+n]
            if (destination[1] == 'n' or destination[1] == 'c') :
                source[0] -= 1
                destination[0] += 1
                destination[1] = 'c'
                if (source[0] == 0) :
                    source[1] = 'n'
            else:
                if (destination[0] > 1) :
                    print "Invalid move - occupied"
                    return -1
                else:
                    bar = self.allSpaces[0]
                    if (destination[1] == 'p') :
                        bar[2] += 1
                    destination[1] = 'c'
                    source[0] -= 1
                    if (source[0] == 0) :
                        source[1] = 'n'
            return 1
        
    def valid_player_move(self, col, n) :
        bar = self.allSpaces[0]
        if (bar[2] != 0 and col != 0) :
            print "Invalid move - you have pieces on the bar"
            return -1
        else:
            if (col == 0) :
                destination = self.allSpaces[25 - n]
            else :
                destination = self.allSpaces[col - n]
            if (destination[1] == 'c' and destination[0] > 1) :
                print "Invalid move - destination occupied"
                return -1
        return 1
    
    def make_player_move(self, col, n) :
        if (self.valid_player_move(col, n) == -1) :
            print "Can't do the move"
            return -1
        else:
            if (col == 0) :
                bar = self.allSpaces[0]
                bar[2] -= 1
                destination = self.allSpaces[25-n]
            else :
                source = self.allSpaces[col]
                source[0] -= 1
                if (source[0] == 0) :
                    source[1] = 'n'
                destination = self.allSpaces[col - n]
            if (destination[1] == 'c' and destination[0] == 1) :
                destination[1] = 'p'
                bar[0] += 1
            else :
                destination[0] += 1
                destination[1] = 'p'
                                  
                
            