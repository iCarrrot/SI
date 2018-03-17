from collections import deque
from random import randint
board = []
dirValue = {'U': (0, 1), 'D': (0, -1), 'R': (-1, 0), 'L': (1, 0)}
meanMoves = {'S':'DURL', 'D':'DRL', 'U': 'URL', 'R':'DUR', 'L':'DUL'} 
startSet = set()
endSet = set()

def prepareData(startSet, endSet, board):
    with open("/home/michal/SI/lab2/zad_input.txt") as f:
        for line in f:
            board.append(line[:-1])
    _x, _y = 0, 0
    for row in board:
        _x = 0
        for l in row:
            if l == 'S':
                startSet.add((_x, _y))
            elif l == 'G':
                endSet.add((_x, _y))
            elif l == 'B':
                endSet.add((_x, _y))
                startSet.add((_x, _y))
            _x += 1
        _y += 1


def move(pos, _dir):
    x, y = pos
    x1, y1 = dirValue[_dir]
    if board[y-y1][x-x1] != '#':
        (x, y) = (x-x1, y-y1)
    if (x, y) in endSet:
        return (x, y), 1
    return (x, y), 0


def moves(posSet, _dir):
    onGoal = 0
    posSet = list(posSet)
    for i in range(len(posSet)):
        posSet[i], _inG = move(posSet[i], _dir)
        onGoal += _inG
    if onGoal == len(posSet):
        return set(posSet), 1
    return set(posSet), 0


def faseOne(startSet):
    final = ""
    mSet = "UDRL"
    for _ in range(len(board)-3):
        startSet, _ = moves(startSet, 'U')
        final+='U'
    for _ in range(len(board[0])-3):
        startSet, _ = moves(startSet, 'R')
        final+='R'
    for _ in range(len(board)):
        startSet, _ = moves(startSet, 'U')
        final+='U'
    # for _ in range(len(board)*2):
    #     a = randint(0,3)
    #     c = mSet[a]
    #     startSet, _ = moves(startSet, c)
    #     final+=c
    return startSet, final


def faseOneAndHalf(startSet):
    visited = []
    visited+=[startSet]
    queue = deque()
    queue.append((startSet,'S'))
    onGoal = 0
    length = 0
    while(not onGoal):
        (posSet, oldM) = queue[0]
        if(len(oldM)>length):
            length+=1
            print(length)
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





def faseTwo(startSet):
    visited = dict()
    visited[tuple(sorted(startSet))] = 1
    queue = deque()
    queue.append((startSet,'S'))
    onGoal = 0
    length = 0
    while(not onGoal):
        (posSet, oldM) = queue[0]
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
            if tuple(sorted(newPos)) not in visited:
                queue.append((newPos,oldM+m))
                visited[tuple(sorted(newPos))] = 1
        queue.popleft()
    return oldM[1:]




def solver():
    final = ''
    startSet = set()
    prepareData(startSet, endSet, board)
    # print(list(startSet))
    startSet, _final = faseOne(startSet)
    final+=_final
    print(final)

    # startSet, _final = faseOneAndHalf(startSet)
    # final+=_final
    # print(final)
    print(list(startSet))
    
    final += faseTwo(startSet)
    # final+="DRRRRDRRRRRRURRD"
    file = open("zad_output.txt", "w")
    file.write(final)
    file.close()
# board = []
solver()