import board


class Bot :
    
    board = board.Board()
    level = 0
    
    def __init__(self, level):
        self.level = level
        
    
    def check_bar(self) :
        bar = self.board.allSpaces[0]
        if (bar[0] != 0) :
            return True
        return False 
    
    def go_towards_house(self, dice) :
        i = 1
        t = False
        while (t == False and i < 24) :
            if (self.board.allSpaces[i][1] != self.board.computer) :
                i += 1
            else :
                if (self.board.allSpaces[i+dice][1] == self.board.computer or 
                    self.board.allSpaces[i+dice][1] == self.board.empty or 
                    (self.board.allSpaces[i+dice][1] == self.board.player and 
                     self.board.allSpaces[i+dice][0] == 1)) :
                    t = True
                else :
                    i += 1
        if (t == True) :
            self.board.make_move(i, dice)
        return
    
    def make_gate(self, dice1, dice2) :
        i = 1
        t = False
        dif = abs(dice1-dice2)
        while (t == False and i < 24) :
            if (self.board.allSpaces[i][1] == self.board.computer and 
                self.board.allSpaces[i+dif][1] == self.board.computer) :
                #posibila poarta
                if (self.board.allSpaces[i + max(dice1, dice2)][1] == self.board.empty or 
                    (self.board.allSpaces[i + max(dice1, dice2)][1] == self.board.player and 
                     self.board.allSpaces[i + max(dice1, dice2)][0] == 1 )) :
                    t = True
                else :
                    i += 1  
            else:
                i += 1
                
        if (t == True) :
            self.board.make_move(i, max(dice1, dice2))
            self.board.make_move(i + dif, min(dice1, dice2))
            print "Made gaaate!"
            return True
        else :
            return False
        
        
    def compute_move(self, dices) :
        if (dices[0] == dices[1]) :
            dice_usage = [False, False, False, False]
        else :
            dice_usage = [False, False]
        
        while (dice_usage.count(False) != 0) :
            
            if (self.check_bar() == False) :
                # compute move
                print "You can compute your move normally"
                if (dices[0] != dices[1] and dice_usage[0] == False and dice_usage[1] == False and 
                    self.make_gate(dices[0], dices[1]) == True) :
                        print "Made gaaate!"
                        dice_usage[1] = True
                        dice_usage[0] = True
                else:
                    dice_index = dice_usage.index(False)
                    self.go_towards_house(dices[dice_index])
                    dice_usage[dice_index] = True
            else :
                # try to move piece from bar
                print "You have to move your piece(s) from the bar first"           
        return
    
    
        
bot = Bot(1)    


# bot.board.printb()
    
movement = 0

while (movement != '-') :
    #player move

    dices = bot.board.generate_dices()
    
    bot.board.printb()
    
    print "Dices = ", dices[0], " ", dices[1]
    
    #Test : player destinations for 24:
    
    #destinations = bot.board.get_player_destinations(24)
    #print "Destinations = ", destinations
    
    movement = input("Player Move: ")
    
    for i in range (0, len(movement), 2) :
        bot.board.move_player(movement[i], movement[i + 1]) 
        
        
    # computer move
    
    dices = bot.board.generate_dices()
    
    
        
    print "Dices = ", dices[0], " ", dices[1]
    
    bot.compute_move(dices)
    
     


