from collections import deque
from queue import PriorityQueue
from random import randint
board = []
dirValue = {'U': (0, 1), 'D': (0, -1), 'R': (-1, 0), 'L': (1, 0)}
meanMoves ="DURL"# {'S': 'DURL', 'D': 'DRL', 'U': 'URL', 'R': 'DUR', 'L': 'DUL'}

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
    # print(dists)
    while len(queue):
        (x, y) = queue[0]
        # print(x, y)
        for x1, y1 in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if dists[y-y1][x-x1] == -1 and (x-x1, y-y1) not in visited:
                visited.add((x-x1, y-y1))
                dists[y-y1][x-x1] = dists[y][x]+1
                queue.append((x-x1, y-y1))
        # print(dists)

        queue.popleft()
    # print(dists)
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
    length = 0
    while(not onGoal):
        (_,_, posSet, oldM) = queue.get()
        # visited.add(posSet)
        # print(visited)
        # print(posSet)
        for m in meanMoves:
            newPos, onGoal = moves(posSet, m)
            if onGoal:
                return oldM[1:]+m
            if newPos not in visited:

                queue.put((len(oldM)+n*heuristic(newPos, dists), len(oldM), newPos, oldM+m))
                # print("  ", len(oldM)+heuristic(newPos, dists),
                #       len(oldM), heuristic(newPos, dists), newPos, oldM+m)
                visited.add(newPos)

    return oldM[1:]


def solver():
    final = ''
    startTuple = ()
    startTuple, dists = prepareData(startTuple, endDict, board)
    dists = findDists(dists)

    # print(dists)

    final += Astar(startTuple, dists, 2)
    # print(list(startTuple))
    # _, _final = faseOne(startTuple)

    # for m in _final:
    #     startTuple, _ = moves(startTuple, m)

    # final+=_final
    # print(final)
    # print(startTuple)

    # final += faseTwo(startTuple)
    # final+="DRRRRDRRRRRRURRD"
    # print(final)
    file = open("zad_output.txt", "w")
    file.write(final)
    file.close()


# board = []
solver()
