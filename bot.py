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
        b.make_player_move(movement[i], movement[i + 1]) 
        
        
    # computer move
    
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    
    for i in range(25):
        print i, " ", b.allSpaces[i]
        
    print "Dices = ", dice1, " ", dice2
    movement = input("Computer Move: ")
    
    for i in range (0, len(movement), 2) :
        b.make_computer_move(movement[i], movement[i + 1]) 
     


