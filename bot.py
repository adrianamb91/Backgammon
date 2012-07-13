import board
import random

b = board.Board()
for i in range(25):
    print i, " ", b.allSpaces[i]
    
movement = 0

while (movement != '-') :
    #player move

    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    
    for i in range(25):
        print i, " ", b.allSpaces[i]
        
    print "Dices = ", dice1, " ", dice2
    movement = input("Player Move: ")
    
    for i in range (0, len(movement), 2) :
        b.move_player(movement[i], movement[i + 1]) 
        
        
    # computer move
    
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    
    if (dice1 == dice2) :
        dices = (dice1, dice1, dice1, dice1)
    else :
        dices = (dice1, dice2)
    
    for i in range(25):
        print i, " ", b.allSpaces[i]
        
    print "Dices = ", dice1, " ", dice2
    
    b.compute_move(dices)
    
     


