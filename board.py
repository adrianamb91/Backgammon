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
    
    def make_player_move(self, col, n) :
        source = self.allSpaces[col]
        if (col > 0 and (source[0] == 0 or 'p' != source[1])) :
            print "Invalid move - invalid source"
            return -1
        elif (col-n < 1) :
            print "Invalid move - invalid destination"
            return -1
        else:
            destination = self.allSpaces[col-n]
            if (destination[1] == 'n' or destination[1] == 'p') :
                # we can do the move
                source[0] -= 1
                destination[0] += 1
                destination[1] = 'p'
                if (source[0] == 0) :
                    source[1] = 'n'
            else:
                if (destination[0] > 1) :
                    #we can't do the move
                    print "Invalid move - occupied"
                    return -1
                else:
                    # we can do the move and we put the other player on the bar
                    bar = self.allSpaces[0]
                    if (destination[1] == 'c') :
                        bar[0] += 1
                    destination[1] = 'p'
                    source[0] -= 1
                    if (source[0] == 0) :
                        source[1] = 'n'
            return 1
                    
                
            