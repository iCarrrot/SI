import random
import sys
from collections import defaultdict as dd
import copy
import time

BOK = 30
SX = -100
SY = 0
M = 8


def initial_board():
    B = [[None] * M for _ in range(M)]
    B[3][3] = 1
    B[4][4] = 1
    B[3][4] = 0
    B[4][3] = 0
    return B


class Board:
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def __init__(self):
        self.board = initial_board()
        self.fields = set()
        self.last_moves = ("nothing", "nothing")
        self.revNum = [2, 2]
        for i in range(M):
            for j in range(M):
                if self.board[i][j] == None:
                    self.fields.add((j, i))

    def draw(self):
        for i in range(M):
            res = []
            for j in range(M):
                b = self.board[i][j]
                # print b
                if b == None:
                    res.append('.')
                elif b == 1:
                    res.append('#')
                else:
                    res.append('o')
            print ''.join(res)
        print

    def moves(self, player):
        res = []
        for (x, y) in self.fields:
            if any(self.can_beat(x, y, direction, player) for direction in Board.dirs):
                res.append((x, y))
        if not res:
            return [None]
        return res

    def can_beat(self, x, y, d, player):
        dx, dy = d
        x += dx
        y += dy
        cnt = 0
        while self.get(x, y) == 1-player:
            x += dx
            y += dy
            cnt += 1
        return cnt > 0 and self.get(x, y) == player

    def get(self, x, y):
        if 0 <= x < M and 0 <= y < M:
            return self.board[y][x]
        return None

    def do_move(self, move, player):
        self.last_moves = (self.last_moves[1], move)
        # print move
        if move == [None] or move == None:
            return
        x, y = move
        x0, y0 = move
        self.board[y][x] = player
        self.revNum[player] += 1
        self.fields -= set([move])
        for dx, dy in self.dirs:
            x, y = x0, y0
            to_beat = []
            x += dx
            y += dy
            while self.get(x, y) == 1-player:
                to_beat.append((x, y))
                x += dx
                y += dy
            if self.get(x, y) == player:
                for (nx, ny) in to_beat:
                    self.board[ny][nx] = player
                    self.revNum[player] += 1
                    self.revNum[1-player] -= 1

    def result(self):

        return self.revNum[1] - self.revNum[0]

    def terminal(self):
        if not self.fields:
            return True
        return self.last_moves[1] == self.last_moves[0] == [None]

    def random_move(self, player):
        ms = self.moves(player)
        if ms and ms != [None]:
            return random.choice(ms)
        return [None]

    def greedy_move(self, player):
        ms = self.moves(player)
        # print player, ms
        if ms != [None] and ms:
            _max, bestM = 0, tuple()
            for (m, cnt) in ms:
                if cnt > _max:
                    _max, bestM = cnt, m
            return bestM
        return [None]

    def heuristicMove(self, player):
        ms = self.moves(player)
        # print ms
        if ms and ms != [None]:
            res = []
            for move in ms:
                res.append((val(nextS(self, move, player), player), move))

            def max_fn(value): return value[0]
            return max(res, key=max_fn)[1]
        return [None]

    def alfabetamove(self, player, depth):
        ms = self.moves(player)
        # print ms
        if ms and ms != [None]:
            res = []
            for move in ms:
                res.append((alphabeta(nextS(self, move, player),depth, -float('Inf'), float('Inf'), 1-player), move))

            def max_fn(value): return value[0]
            return max(res, key=max_fn)[1]
        return [None]

def alphabeta(state, depth, alpha, beta, player):
    if state.terminal():
        return float("Inf")
    if depth == 0:
        return heuristic_value(state,1-player)

    if player:
        v = -float("Inf")
        for m in state.moves(player):
            child = nextS(state,m,player)
            v = max(v, alphabeta(child, depth - 1, alpha, beta, 1-player))
            alpha = max(alpha, v)
            if beta <= alpha:
                break 
        return v
    else:
        v = float("Inf")
        for m in state.moves(player):
            child = nextS(state,m,player)
            v = min(v, alphabeta(child, depth - 1, alpha, beta, player))
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v

def nextS(state, move, player):
    nextS = copy.deepcopy(state)
    nextS.do_move(move, player)
    return nextS


def val(current_state, player):
    if current_state.terminal():
        return float("Inf")
    return heuristic_value(current_state, player)


def corners(state, player):
    res = 0
    for (i, j) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
        if state.board[i][j] == player:
            res += 1
    return res


def corners_neighbours(state, player):
    res = 0
    cornerDict = {
        (0, 0): [(1, 0), (0, 1), (1, 1)],
        (0, 7): [(1, 7), (0, 6), (1, 6)],
        (7, 0): [(7, 1), (6, 0), (6, 1)],
        (7, 7): [(7, 6), (6, 7), (6, 6)]
    }
    for (i, j) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
        if state.board[i][j] == None:
            for el in cornerDict[(i, j)]:
                (i1, j1) = el
                if state.board[i1][j1] == player:
                    res += 1
                if (i1 == 1 or i1 == 6) and (j1 == 1 or j1 == 6):
                    res += 1
    return res


def heuristic_value(state, player):
    if state.terminal():
        return state.result()*float("Inf")
    res = 0
    coin_parity = float(state.result()) / \
        sum(state.revNum)  # procent pionków

    ending = (sum(state.revNum) > 55) * coin_parity

    corners_captured = corners(state, player) \
        - corners(state, 1-player)

    mobility = len(state.moves(player)) \
        - len(state.moves(1-player))

    corners_neighbourhood = corners_neighbours(state, player) \
        - corners_neighbours(state, 1-player)

    res += 10 * corners_captured \
        + 1 * mobility \
        - 5 * corners_neighbourhood \
        + 1 * ending
    return res


def playGame(player, B):
    while True:
        if not player:
            m = B.random_move(player)
        else:
            m = B.alfabetamove(player=player,depth=1)
            # m = B.heuristicMove(player=player)
        # print m
        if m and m != None:
            B.do_move(m, player)
        player = 1-player
        # B.draw()
        # raw_input()
        if B.terminal():
            break


defs = 0
tries = 10000
start_time = time.time()
for i in range(1, tries+1):
    player = 0
    B = Board()
    playGame(player=player, B=B)

    # B.draw()
    # B.show()
    r = B.result()

    if r < 0:
        defs += 1

    # raw_input('Game over!')
    if not i % 5:
        print i, ': Result', r, defs
        print("--- %s seconds ---" % (time.time() - start_time))

    # sys.exit(0)
print 100 - 100.*defs/tries, "% wygranych"
