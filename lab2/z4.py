from collections import deque
from random import randint
board = []
dirValue = {'U': (0, 1), 'D': (0, -1), 'R': (-1, 0), 'L': (1, 0)}
meanMoves = {'S':'DURL', 'D':'DRL', 'U': 'URL', 'R':'DUR', 'L':'DUL'} 
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


def faseOne(startTuple):
    final = ""
    # print(startTuple)
    
    # startTuple, _ = moves(startTuple, 'R')
    
    # mSet = "UDRL"
    for _ in range(len(board)-3):
        startTuple, _ = moves(startTuple, 'U')
        final+='U'
    for _ in range(len(board[0])-3):
        startTuple, _ = moves(startTuple, 'R')
        final+='R'
    for _ in range(len(board)):
        startTuple, _ = moves(startTuple, 'U')
        final+='U'
    # print(len(startTuple))
    # for _ in range(len(board)*2):
    #     a = randint(0,3)
    #     c = mSet[a]
    #     startTuple, _ = moves(startTuple, c)
    #     final+=c
    return startTuple, final


def faseOneAndHalf(startTuple):
    visited = []
    visited+=[startTuple]
    queue = deque()
    queue.append((startTuple,'S'))
    onGoal = 0
    length = 0
    while(not onGoal):
        (posSet, oldM) = queue[0]
        if(len(oldM)>length):
            length+=1
            # print(length)
        # print (posSet)
        # print (oldM)
        other= []
        for m in meanMoves[oldM[-1]]:
            newPos, onGoal = moves(posSet, m)
            if(len(newPos)<len(posSet)):
                if onGoal or len(newPos) == 1:
                    return newPos, oldM[1:]+m
                if newPos not in visited:
                    queue.append((newPos,oldM+m))
                    visited+=[newPos]
            else:
                other += [(newPos, onGoal)]
        if len(other) >= 3:
            for (newPos, onGoal) in other:
                if onGoal or len(newPos) == 1:
                    return newPos, oldM[1:]+m
                if newPos not in visited:
                    queue.append((newPos,oldM+m))
                    visited+=[newPos]
        queue.popleft()
    return newPos, oldM[1:]





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
        if(len(oldM)>length):
            length+=1
            print(length)
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
    # print(list(startTuple))
    startTuple, _final = faseOne(startTuple)
    final+=_final
    print(final)

    # startTuple, _final = faseOneAndHalf(startTuple)
    # final+=_final
    # print(final)
    # print(list(startTuple))
    
    final += faseTwo(startTuple)
    # final+="DRRRRDRRRRRRURRD"
    file = open("zad_output.txt", "w")
    file.write(final)
    file.close()
# board = []
solver()