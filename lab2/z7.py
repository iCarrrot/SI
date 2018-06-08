from collections import deque
from queue import PriorityQueue
from random import randint
board = []
dirValue = {'U': (0, 1), 'D': (0, -1), 'R': (-1, 0), 'L': (1, 0)}

startTuple = ()
endDict = dict()


def prepareData(startTuple, endDict, board):
    with open("/home/michal/SI/lab2/zad_input.txt") as f:
        for line in f:
            board.append(line[:-1])
    _x, _y = 0, 0
    dists = [[-10 for _ in board[0]] for _ in board]
    for row in board:
        _x = 0
        for l in row:
            if l == 'S':
                startTuple += ((_x, _y),)
                dists[_y][_x] = -1
            elif l == 'G':
                endDict[(_x, _y)] = 1
                dists[_y][_x] = 0
            elif l == 'B':
                endDict[(_x, _y)] = 1
                startTuple += ((_x, _y),)
                dists[_y][_x] = 0
            elif l == ' ':
                dists[_y][_x] = -1
            _x += 1
        _y += 1
    return startTuple, dists


def faseOne(startTuple, _range = 100, _size = 64):

    startTuple1 = startTuple
    final1 = ""
    for _ in range(len(board)-3):
        startTuple1, _ = moves(startTuple1, 'U')
        final1+='U'
    for _ in range(len(board[0])-3):
        startTuple1, _ = moves(startTuple1, 'R')
        final1+='R'

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
                    testTuple2, _ = moves(testTuple2, move)
                    if len(testTuple2)<= minLen2:
                        minTuple2 = testTuple2
                        minLen2 = len(testTuple2)
                        minM = move
                testTuple = minTuple2
                randomSet+=minM

        if len(testTuple)< minLen:
            minTuple = testTuple
            minLen = len(testTuple)
            minFinal = randomSet
    startTuple = minTuple
    final += minFinal
    return startTuple, final



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
    for i in posSet:
        t, _inG = move(i, _dir)
        onGoal += _inG
        tempList += [t]

    if onGoal == len(posSet):
        return tuple(set(sorted(tempList))), 1
    return tuple(set(sorted(tempList))), 0


def findDists(dists):
    queue = deque()
    visited = set()
    for x, y in endDict:
        visited.add((x, y))
        for x1, y1 in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if dists[y-y1][x-x1] == -1 and (x-x1, y-y1) not in visited:
                dists[y-y1][x-x1] = 1
                queue.append((x-x1, y-y1))
                visited.add((x-x1, y-y1))
    while len(queue):
        (x, y) = queue[0]
        for x1, y1 in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if dists[y-y1][x-x1] == -1 and (x-x1, y-y1) not in visited:
                visited.add((x-x1, y-y1))
                dists[y-y1][x-x1] = dists[y][x]+1
                queue.append((x-x1, y-y1))
        queue.popleft()
    return dists


def heuristic(currentTuple, dists):
    _max = 0
    for x, y in currentTuple:
        if dists[y][x] > _max:
            _max = dists[y][x]
    return _max


def Astar(startTuple, dists, n):
    visited = set()
    visited.add(startTuple)

    queue = PriorityQueue()
    queue.put((heuristic(startTuple, dists),0, startTuple, 'S'))
    onGoal = 0
    while(not onGoal):
        (_,_, posSet, oldM) = queue.get()
        for m in "UDRL":
            newPos, onGoal = moves(posSet, m)
            if onGoal:
                return oldM[1:]+m
            if newPos not in visited:

                queue.put((len(oldM)+n*heuristic(newPos, dists), len(oldM), newPos, oldM+m))
                visited.add(newPos)

    return oldM[1:]


def solver():
    final = ''
    startTuple = ()
    startTuple, dists = prepareData(startTuple, endDict, board)
    dists = findDists(dists)
    
    _, _final = faseOne(startTuple, _size=1)
    for m in _final:
        startTuple, _ = moves(startTuple, m)
    final+=_final

    final += Astar(startTuple, dists, 2.5)

    file = open("zad_output.txt", "w")
    file.write(final)
    file.close()
    file = open("result.txt", "r")
    lines = file.readlines()
    file.close()
    
    file = open("result.txt", "w")
    
    # print lines
    lines+=[final]
    newlines = "\n".join(lines)
    # print newlines
    file.write(newlines)
    file.close()
    


# board = []
solver()
