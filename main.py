import board

b = board.Board()
for i in range(25):
    print i, " ", b.allSpaces[i]
    
movement = input("Move: ")

while (len(movement) == 3) :
    if (movement[0] == 'c') :
        b.make_computer_move(movement[1], movement[2])
    else :
        b.make_player_move(movement[1], movement[2]) 
    for i in range(25):
        print i, " ", b.allSpaces[i]
    
    movement = input("Move: ")

