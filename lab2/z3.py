from collections import deque
from queue import PriorityQueue

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



def Kmoves(pos, boxTuple):
    queue = deque()
    avible = dict()
    avible[pos] = ""
    queue.append((pos),)
    # print(board)
    while len(queue):
        (x, y) = queue[0]
        # print(x, y)
        for m in dirValue:
            x1, y1 = dirValue[m]
            if board[y-y1][x-x1] != "W" and (x-x1, y-y1) not in avible and (x-x1, y-y1) not in boxTuple:
                avible[(x-x1, y-y1)] = avible[(x, y)] + m
                queue.append((x-x1, y-y1))
        queue.popleft()
    # print(board)
    return avible


def bestFirstSearch(startPos, startBoxTuple, dists):
    visited = set()
    visited.add(tuple(set(startBoxTuple)))
    queue = PriorityQueue()
    queue.put((heuristic(startBoxTuple, dists), 0,
               startPos, startBoxTuple, 'S'),)
    # onGoal = 0
    length = 0
    a = 0
    while(not queue.empty()):
        (_, level, pos, boxTuple, way) = queue.get()
        # visited.add(posSet)
        # print(visited)
        # print(posSet)
        avible = Kmoves(pos, boxTuple)
        # print(avible)
        # print(level)
        # if(level >= length):
        #     length += 1
            # print(length)

        for box in boxTuple:
            for m in "UDLR":
                # a+=1
                # print("  ",a)
                semiNewPos, newBoxTuple, info = moveBox(
                    box, boxTuple, m, avible)
                newPos = box
                # print(newBoxTuple)
                if info > 0:
                    # print(newPos, semiNewPos, newBoxTuple, goals, info, way)
                    return way[1:]+avible[semiNewPos] + m
                elif info>=0 and tuple(set(newBoxTuple)) not in visited:
                    queue.put((heuristic(newBoxTuple, dists), level+1,
                               newPos, newBoxTuple, way+avible[semiNewPos]+m),)
                    visited.add(tuple(set(newBoxTuple)))
                    # print(visited)
                # elif (newPos, newBoxTuple) not in visited:
                #     print(newPos, semiNewPos, newBoxTuple, goals, info, way)

    print(len(visited))
    return way[1:]


def moveBox(box, boxTuple, direction, avible):
    x, y = box
    x1, y1 = x + dirValue[direction][0], y + dirValue[direction][1]
    if (x1, y1) in avible:
        x2, y2 = x - dirValue[direction][0], y - dirValue[direction][1]
        
        if board[y2][x2] != 'W' and (x2, y2) not in boxTuple and not isInCorner((x2, y2)):
            temp = tuple()
            onGoal = 0
            # print(boxTuple)
            for _box in boxTuple:
                if _box == (x, y):
                    temp = temp + ((x2, y2),)
                    if (x2, y2) in goals:
                        onGoal += 1
                else:
                    if _box in goals:
                        onGoal += 1
                    temp = temp + (_box,)
            # print(onGoal, len(boxTuple))
            # if onGoal == len(boxTuple):
                # print(onGoal, boxTuple, goals)
            # 2*(onGoal == len(boxTuple)) - isInCorner((x2,y2))
            return (x1, y1), temp, onGoal == len(boxTuple)
        # if board[y2][x2] != 'W' and (x2, y2) not in boxTuple and isInCorner((x2, y2)):
        #     print(x2,y2)
    return (0, 0), 0, -1

def isInCorner(box):
    i, j = box
    # print(i,j)
    if(box not in goals):
        if(any(board[p[1]][p[0]] == "W" for p in [(i, j-1), (i, j+1)]) and (any(board[p[1]][p[0]] == "W" for p in [(i-1, j), (i+1, j)]))):
            return True
    return False


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


def solver():
    final = ''
    boxTuple, pos, dists = prepareData()
    dists = findDists(dists)
    final = bestFirstSearch(pos, boxTuple, dists)
    # print(final)
    file = open("zad_output.txt", "w")
    file.write(final)
    file.close()


solver()
