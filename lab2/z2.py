from collections import deque
from queue import PriorityQueue
import sys

board = []
dirValue = {'U': (0, 1), 'D': (0, -1), 'R': (-1, 0), 'L': (1, 0)}
goals = set()


def prepareData():
    with open("/home/michal/SI/lab2/zad_input.txt") as f:
        for line in f:
            board.append(line[:-1])
    _x, _y = 0, 0
    boxTuple = tuple()
    pos = (0, 0)
    dists = [[-1 for _ in board[0]] for _ in board]
    for row in board:
        _x = 0
        for l in row:
            if l == 'B':
                boxTuple += ((_x, _y),)

            elif l == 'G':
                goals.add((_x, _y),)
                dists[_y][_x] = 0
            elif l == '*':
                goals.add((_x, _y),)
                dists[_y][_x] = 0
                boxTuple += ((_x, _y),)
            elif l == "+":
                pos = (_x, _y)
                goals.add((_x, _y),)
            elif l == "K":
                pos = (_x, _y)
            elif l == "W":
                dists[_y][_x] = -10
            _x += 1
        _y += 1
    return boxTuple, pos, dists




def move(pos, boxTuple, direction):
    x, y = pos
    x1, y1 = x - dirValue[direction][0], y - dirValue[direction][1]
    if (x1, y1) in boxTuple:
        x2, y2 = x1 - dirValue[direction][0], y1 - dirValue[direction][1]
        if board[y2][x2] != 'W' and (x2, y2) not in boxTuple:
            temp = tuple()
            inGoal = 0
            for box in boxTuple:

                if box == (x1, y1):
                    temp = temp + ((x2, y2),)
                    if (x2, y2) in goals:
                        inGoal += 1
                else:
                    if box in goals:
                        inGoal += 1
                    temp = temp + (box,)
            # print(inGoal, len(boxTuple))
            # 2*(inGoal == len(boxTuple)) - isInCorner((x2,y2))
            return (x1, y1), temp, inGoal == len(boxTuple)
        else:
            return (x, y), boxTuple, 0
    else:
        if board[y1][x1] != 'W':
            return (x1, y1), boxTuple, 0
        return (x, y), boxTuple, 0


def bfs(startPos, startBoxTuple):
    visited = set()
    visited.add((startPos, startBoxTuple),)
    queue = deque()
    queue.append((startPos, startBoxTuple, "S"),)
    length = 0
    while(len(queue) > 0):

        pos, boxTuple, way = queue[0]

        if(len(way) > length):
            length += 1
            # print(length)

        for m in "UDLR":
            newPos, newBoxTuple, info = move(pos, boxTuple, m)

            if info > 0:
                # print(newPos, newBoxTuple, goals, info, way)
                return way[1:]+m
            elif (newPos, newBoxTuple) not in visited:
                queue.append((newPos, newBoxTuple, way+m))
                visited.add((newPos, newBoxTuple),)
        queue.popleft()
    # return way[1:]


def findDists(dists):
    queue = deque()
    visited = set()
    for x, y in goals:
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
    _sum = 0
    for x, y in currentTuple:
        _sum = dists[y][x]
    return _sum


def Astar(startPos, startBoxTuple, dists):
    visited = set()
    visited.add((startPos, startBoxTuple),)
    queue = PriorityQueue()
    queue.put((heuristic(startBoxTuple, dists),
               0, (startPos, startBoxTuple), 'S'))
    onGoal = 0
    while(not onGoal):
        (_, _, (pos, boxTuple), way) = queue.get()
        # visited.add(posSet)
        # print(visited)
        # print(posSet)
        for m in "UDLR":
            newPos, newBoxTuple, info = move(pos, boxTuple, m)
            if info > 0:
                # print(newPos, newBoxTuple, goals, info, way)
                return way[1:]+m
            elif (newPos, newBoxTuple) not in visited:

                queue.put((len(way)+heuristic(newBoxTuple, dists),
                           len(way), (newPos, newBoxTuple), way+m))
                # print("  ", len(oldM)+heuristic(newPos, dists),
                #       len(oldM), heuristic(newPos, dists), newPos, oldM+m)
                visited.add((newPos, newBoxTuple),)

    return way[1:]


def solver():
    final = ''
    boxTuple, pos, dists = prepareData()
    # print(sys.argv)
    # print(boxTuple,pos)
    # print(goals, len(goals))
    if sys.argv[1] == "bfs":
        final = bfs(pos, boxTuple)
    elif sys.argv[1] == "a*":
        final = Astar(pos, boxTuple, dists)
    # print(final)
    file = open("zad_output.txt", "w")
    file.write(final)
    file.close()


solver()
