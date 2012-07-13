class Board:  
    allSpaces = []
    def __init__(self):
        for i in range(25):
            self.allSpaces.insert(i, (0, 'n')) # n = nothing
            
        self.allSpaces[0] = (0, 'c', 0, 'p') # bar
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
            
            
    def make_move(self, col, n) :
        source = self.allSpaces[col]
        if (col > 0 and (source[0] == 0 or 'c' != source[1])) :
            print "Invalid move - invalid source"
            return False
        elif (col+n < 0) :
            print "Invalid move - invalid destination"
            return False
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
                    return False
                else:
                    bar = self.allSpaces[0]
                    if (destination[1] == 'p') :
                        bar[2] += 1
                    destination[1] = 'c'
                    source[0] -= 1
                    if (source[0] == 0) :
                        source[1] = 'n'
            return True
        
    def check_bar(self) :
        b = self.allSpaces[0]
        if (b[0] != 0) :
            return True
        return False
    
    def go_towards_house(self, dice) :
        i = 1
        t = False
        while (t == False and i < 25) :
            if (self.allSpaces[i][1] != 'c') :
                i += 1
            else :
                if (self.allSpaces[i+dice][1] == 'c' or self.allSpaces[i+dice][1] == 'n' 
                    or (self.allSpaces[i+dice][1] == 'p' and self.allSpaces[i+dice][0] == 1)) :
                    t = True
                else :
                    i += 1
        if (i < 25) :
            self.make_move(i, dice)
        return
    
    def compute_move(self, dices) :
        if (dices[0] == dices[1]) :
            dice_usage = [False, False, False, False]
        else :
            dice_usage = [False, False]
        
        while (dice_usage.count(False) != 0) :
            
            if (self.check_bar() == False) :
                # compute move
                print "You can compute your move normally"
                dice_index = dice_usage.index(False)
                self.go_towards_house(dices[dice_index])
                dice_usage[dice_index] = True
            else :
                # try to move piece from bar
                print "You have to move your piece(s) from the bar first"
                
        return
    
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
            if (destination[1] == 'c' and destination[0] > 1) :
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
                    source[1] = 'n'
                destination = self.allSpaces[col - n]
            if (destination[1] == 'c' and destination[0] == 1) :
                destination[1] = 'p'
                bar[0] += 1
            else :
                destination[0] += 1
                destination[1] = 'p'
        return True
                                  
                
            