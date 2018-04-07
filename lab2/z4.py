from collections import deque
from random import randint, seed

board = []
dirValue = {'U': (0, 1), 'D': (0, -1), 'R': (-1, 0), 'L': (1, 0)}
meanMoves = {'S':'DURL', 'D':'DURL', 'U': 'DURL', 'R':'DURL', 'L':'DURL'} 
startTuple = ()
endDict = dict()


def prepareData(startTuple, endDict, board):
    with open("/home/michal/SI/lab2/zad_input.txt") as f:
        for line in f:
            board.append(line[:-1])
    _x, _y = 0, 0
    for row in board:
        _x = 0
        for l in row:
            if l == 'S':
                startTuple+=((_x, _y),)
            elif l == 'G':
                endDict[(_x, _y)] =1
            elif l == 'B':
                endDict[(_x, _y)] =1
                startTuple+=((_x, _y),)
            _x += 1
        _y += 1
    return startTuple


def move(pos, _dir):
    x, y = pos
    x1, y1 = dirValue[_dir]
    if board[y-y1][x-x1] != '#':
        (x, y) = (x-x1, y-y1)
    if (x, y) in endDict:
        return (x, y), 1
    return (x, y), 0


def moves(posSet, _dir):
    onGoal = 0
    tempList = []
    # print("p", posSet)
    for i in posSet:
        # print(i)
        t, _inG = move(i, _dir)
        # print(t)
        onGoal += _inG
        tempList+=[t]

    if onGoal == len(posSet):
        return tuple(set(sorted(tempList))), 1
    return tuple(set(sorted(tempList))), 0


def faseOne(startTuple, _range = 100, _size = 64):

    startTuple1 = startTuple
    final1 = ""
    for _ in range(len(board)-3):
        startTuple1, _ = moves(startTuple1, 'U')
        final1+='U'
    for _ in range(len(board[0])-3):
        startTuple1, _ = moves(startTuple1, 'R')
        final1+='R'
    for _ in range(len(board)):
        startTuple1, _ = moves(startTuple1, 'U')
        final1+='U'

    startTuple = startTuple1
    mSet = "UDRL"
    final = final1
    minLen = len(startTuple)
    minTuple = startTuple
    minFinal = ""
    for _ in range(_range):
        testTuple = startTuple
        randomSet = ""
        for i in range(_size):
            if not i%5:
                testTuple, _ = moves(testTuple, mSet[randint(0,3)])
                randomSet += mSet[randint(0,3)]
            else:
                testTuple2 = testTuple
                minLen2 = len(testTuple2)
                for move in mSet:
                    # print(" ")
                    testTuple2, _ = moves(testTuple2, move)
                    if len(testTuple2)<= minLen2:
                        minTuple2 = testTuple2
                        minLen2 = len(testTuple2)
                        minM = move
                    # print("   ", len(testTuple2))
                # print("  ", len(minTuple2))
                testTuple = minTuple2
                randomSet+=minM

        if len(testTuple)< minLen:
            minTuple = testTuple
            minLen = len(testTuple)
            minFinal = randomSet
        # print(len(testTuple))
    startTuple = minTuple
    final += minFinal
    # print("2: ",len(startTuple))
    return startTuple, final



def faseTwo(startTuple):
    visited = dict()
    visited[startTuple] = 1
    queue = deque()
    queue.append((startTuple,'S'))
    onGoal = 0
    length = 0
    # print(queue)
    while(not onGoal):
        (posSet, oldM) = queue[0]
        # print(oldM)
        # print(visited)
        # if(len(oldM)>length):
        #     length+=1
        #     print(length)
        # print (posSet)
        # print (oldM)
        for m in meanMoves[oldM[-1]]:
            newPos, onGoal = moves(posSet, m)
            if onGoal:
                return oldM[1:]+m
            if newPos not in visited:
                queue.append((newPos,oldM+m))
                visited[newPos] = 1
        queue.popleft()
    return oldM[1:]




def solver():
    final = ''
    startTuple = ()
    startTuple = prepareData(startTuple, endDict, board)
    _, _final = faseOne(startTuple)
    for m in _final:
        startTuple, _ = moves(startTuple, m)
    print(startTuple)
    final+=_final
    
    final += faseTwo(startTuple)
    file = open("zad_output.txt", "w")
    file.write(final)
    file.close()

solver()