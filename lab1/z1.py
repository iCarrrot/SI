from collections import deque
debug = 1

def isOnBoard(pos):
    if len(pos) == 2 and pos[0] >= 'a' and pos[0] <= 'h' and pos[1] >= '1' and pos[1] <= '8':
        return True
    return False


def moves(piece, pos):
    if piece == "r":
        if isOnBoard(pos):
            return [chr(c) + pos[1] for c in range(ord('a'), ord(pos[0]))] + \
                [chr(c) + pos[1] for c in range(ord(pos[0]) + 1, ord('h') + 1)] + \
                [pos[0] + str(c) for c in range(1, int(pos[1]))] + \
                [pos[0] + str(c) for c in range(int(pos[1])+1, 8 + 1)]
        else:
            return []
    elif piece == 'k':
        moves = [chr(ord(pos[0]) - 1) + str(int(pos[1])-1),
                 chr(ord(pos[0]) - 1) + str(int(pos[1])),
                 chr(ord(pos[0]) - 1) + str(int(pos[1])+1),
                 chr(ord(pos[0])) + str(int(pos[1])-1),
                 chr(ord(pos[0])) + str(int(pos[1])+1),
                 chr(ord(pos[0]) + 1) + str(int(pos[1])-1),
                 chr(ord(pos[0]) + 1) + str(int(pos[1])),
                 chr(ord(pos[0]) + 1) + str(int(pos[1])+1)
                 ]
        return list(filter(isOnBoard, moves))


def isCheckmate(wk, wr, bk):
    whites = moves('k', wk) + moves('r', wr)
    blacks = moves('k', bk) + [bk]
    for b in blacks:
        if b not in whites:
            return False
    return True


def isCheck(king, rest):
    fMoves = []
    for fig in rest:
        fMoves += moves(fig, rest[fig]) + [rest[fig]]
    if king in fMoves:
        return True
    return False

def findCheckMate(inputData, debug = 0):
    [player, wk, wr, bk] = inputData.split()
    queue = deque([((player, wk, wr, bk), 0)])
    addedMoves = {}
    movesDict = {}
    addedMoves[(player, wk, wr, bk)] = 1
    movesDict[(player, wk, wr, bk)] = ''
    end = False
    steps = 0
    if isCheckmate(wk, wr, bk):
        end = True
    diag_steps = 0
    print(1)
    while not end:
        ((player, wk, wr, bk), steps) = queue[0]
        if steps > diag_steps and debug:
            print(steps+1)
            diag_steps = steps
        if player == "black":
            movesList = list(filter(lambda x: not isCheck(
                x, {'k': wk, 'r': wr}), moves('k', bk)))
            for m in movesList:
                if isCheckmate(wk, wr, m):
                    movesDict[('white', wk, wr, m)] = (player, wk, wr, bk)
                    last = ('white', wk, wr, m)
                    end = True
                    break
                elif ('white', wk, wr, m) not in addedMoves:
                    addedMoves[('white', wk, wr, m)] = 1
                    movesDict[('white', wk, wr, m)] = (player, wk, wr, bk)
                    queue.append((('white', wk, wr, m), steps+1))
        else:
            kMovesList = list(filter(lambda x: not isCheck(
                x, {'k': bk}) and x is not wr, moves('k', wk)))
            for m in kMovesList:
                if isCheckmate(m, wr, bk):
                    movesDict[('black', m, wr, bk)] = (player, wk, wr, bk)
                    last = ('black', m, wr, bk)
                    end = True
                    break
                elif ('black', m, wr, bk) not in addedMoves:
                    addedMoves[('black', m, wr, bk)] = 1
                    movesDict[('black', m, wr, bk)] = (player, wk, wr, bk)
                    queue.append((('black', m, wr, bk), steps+1))
            rMovesList = list(
                filter(lambda x: x is not wk and x is not bk, moves('r', wr)))
            for m in rMovesList:
                if isCheckmate(wk, m, bk):
                    movesDict[('black', wk, m, bk)] = (player, wk, wr, bk)
                    last = ('black', wk, m, bk)
                    end = True
                    break
                elif ('black', wk, m, bk) not in addedMoves:
                    addedMoves[('black', wk, m, bk)] = 1
                    movesDict[('black', wk, m, bk)] = (player, wk, wr, bk)
                    queue.append((('black', wk, m, bk), steps+1))
        queue.popleft()
    if debug:
        move = movesDict[last]
        lista = [last]
        while move is not '':
            lista = [move] + lista
            move = movesDict[move]
        for l in lista:
            print('♔ : ', l[1], '♖ : ', l[2], '♚ : ', l[3])
    return steps+1

with open("input_1.1.txt") as f:
    for line in f:
        print(findCheckMate(line, debug))
