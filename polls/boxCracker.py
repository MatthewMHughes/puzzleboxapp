import random
import math
crackTotals = []
sols = []
for i in range(100):
    movements = [[13, 1], [10, 1], [14, 1], [7, 0], [1, 0], [12, 1], [1, 0], [10, 0]]
    possiblePos = [[13, 19, 25, 7, 1, -5, -11, -17, -23], 
                   [10, 16, 22, 4, -2, -8, -14, -20], 
                   [14, 20, 8, 2, -4, -10, -16, -22],
                   [-7, -13, -19, -25, -1, 5, 11, 17, 23],
                   [-1, -7, -13, -19, -25, 5, 11, 17, 23],
                   [12, 18, 24, 6, 0, -6, -12, -18, -24],
                   [-1, -7, -13, -19, -25, 5, 11, 17, 23],
                   [-10, -16, -22, -4, 2, 8, 14, 20]
                   ]
    dialPistons = [0, 0, 0, 0, 0, 0, 0, 0]
    dialPositions = [0, 0, 0, 0, 0, 0, 0, 0]
    dialMovements =  [[[3, -1], [1, -1]], [[3, -1], [0, -1]], [[5, -1], [3, 1]], [[5, -1], [2, -1]], [[7, -1], [6, 1]], [[3, -1], [4, -1]], [[3, -1], [6, 1]], [[5, -1], [4, -1]]]
    moves = 0
    cracked = False
    moveDial = random.randint(0, 7)
    moveDir = random.randint(0, 1)
    while not cracked:
        changeDir = random.randint(0, 1)
        #50% chance same direction of same dial - 25% change dial - tries to keep dial + direction to best replicate real use
        if changeDir == 1:
            changeDial = random.randint(0, 1)
            if moveDir == 1:
                moveDir = 0
            else:
                moveDir = 1
            if changeDial == 1:
                lastDial = moveDial
                moveDial = random.randint(0, 6)
                if moveDial == lastDial:
                    if moveDial == 0:
                        moveDial = 7
                    else:
                        moveDial-=1
        '''
        #Purely Random
        moveDial = random.randint(0, 7)
        moveDir = random.randint(0, 1)
        '''
        if moveDir == 1 and dialPositions[moveDial] == 25:
            moveDir = 0
        elif moveDir == 0 and dialPositions[moveDial] == -25:
            moveDir = 1
        if moveDir == 1:
            dialPositions[moveDial]+=1
            dialMove = 1
            position = dialPistons[moveDial]
            position += dialMove
            if position == 6:
                position = 0
            if position == -1:
                position = 5
            dialPistons[moveDial] = position
            for movement in dialMovements[moveDial]:
                position = dialPistons[movement[0]]
                position += movement[1]
                if position == 6:
                    position = 0
                if position == -1:
                    position = 5
                dialPistons[movement[0]] = position
        else:
            dialPositions[moveDial]-=1
            dialMove = -1
            position = dialPistons[moveDial]
            position += dialMove
            if position == 6:
                position = 0
            if position == -1:
                position = 5
            dialPistons[moveDial] = position
            for movement in dialMovements[moveDial]:
                position = dialPistons[movement[0]]
                position -= movement[1]
                if position == 6:
                    position = 0
                if position == -1:
                    position = 5
                dialPistons[movement[0]] = position

        if dialPositions[moveDial] > 25 or dialPositions[moveDial] < -25:
            cracked = True
            print("error: dial at position ", moveDial, " is now at ", dialPositions[moveDial])
        if dialPistons == [3, 3, 3, 3, 3, 3, 3, 3]:
            cracked = True
        moves+=1
    print("Took: ", moves, " to crack!")
    print("Positions are: ", dialPositions)
    print("Pistons are: ", dialPistons)
    fitSol = True
    for i in range(8):
        fitNum = False
        for j in range(len(possiblePos[i])):
            if possiblePos[i][j] == dialPositions[i]:
                fitNum = True
        if fitNum == False:
            fitSol = False
    if fitSol:
        print("Position fits solution!")
        sols.append(dialPositions)
    crackTotals.append(moves)
print("fit sols:", sols)
print("number fit sols:", len(sols))

print(crackTotals)
total = 0
for i in crackTotals:
    total+=i
average = total / 100.0
print("average moves is: ", average)
print("lowest is: ", min(crackTotals))
print("highest is: ", max(crackTotals))