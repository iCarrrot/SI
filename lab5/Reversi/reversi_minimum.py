# coding=utf-8
import random
import sys
from collections import defaultdict as dd
import copy
import time
from sklearn.neural_network import MLPClassifier

import pickle

with open('../NN/nn_weights_bigger_more.dat') as f:
    nn = pickle.load(f)

BOK = 30
SX = -100
SY = 0
M = 8

def boardToTab(board):
    res = []
    for y in board:
        res+=y
    return res

def initial_board():
    B = [[0] * M for _ in range(M)]
    B[3][3] = 1
    B[4][4] = 1
    B[3][4] = -1
    B[4][3] = -1
    return B
def addAtributes(data):
    res = []
    #suma
    res.append(sum(data))
    #rogi
    corners1=0
    corners2=0
    for (i, j) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
        if data[i*8+j] == 1:
            corners1 += 1
        if data[i*8+j] == -1:
            corners2 += 1
    res.append(corners1) 
    res.append(corners2)

    # sąsiedzi rogów
    
    cornerDict = {
        (0, 0): [(1, 0), (0, 1), (1, 1)],
        (0, 7): [(1, 7), (0, 6), (1, 6)],
        (7, 0): [(7, 1), (6, 0), (6, 1)],
        (7, 7): [(7, 6), (6, 7), (6, 6)]
    }
    corners_n1 = 0
    corners_n2 = 0
    for (i, j) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
        if data[i*8+j] == 0:
            for el in cornerDict[(i, j)]:
                (i1, j1) = el
                if data[i1*8+j1] == 1:
                    corners_n1 += 1
                    if (i1 == 1 or i1 == 6) and (j1 == 1 or j1 == 6):
                        corners_n1 += 1
                if data[i1*8+j1] == -1:
                    corners_n2 += 1
                    if (i1 == 1 or i1 == 6) and (j1 == 1 or j1 == 6):
                        corners_n2 += 1

    res.append(corners_n1)
    res.append(corners_n2)

    edge1,edge2 = 0,0
    edge_n1, edge_n2 = 0,0
    for i in range(64):
        x,y = i//8, i%8
        if ((x ==1 or x ==6 ) and 1<=y<=6) or  (( y == 1 or y ==6) and 1<=x<=6):
            if data[i] == 1:
                edge1+=1
            if data[i] ==-1:
                edge2+=1

        if ((x ==2 or x ==5 ) and 2<=y<=5) or  (( y == 2 or y ==5) and 2<=x<=5):
            if data[i] == 1:
                edge_n1+=1
            if data[i] ==-1:
                edge_n2+=1
    res+=[edge1,edge2,edge_n1,edge_n2]
    return res+data

class Board:
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def __init__(self):
        self.board = initial_board()
        self.fields = set()
        self.last_moves = ("nothing", "nothing")
        self.revNum = {-1:2, 1:2}
        for i in range(M):
            for j in range(M):
                if self.board[i][j] == 0:
                    self.fields.add((j, i))

    def draw(self, validator = 0):
        if validator:
            for i in range(M):
                res = []
                for j in range(M):
                    b = self.board[i][j]
                    # print b
                    if b == 0:
                        res.append('.')
                    elif b == 1:
                        res.append('X')
                    else:
                        res.append('O')
                sys.stderr.write( ''.join(res))
                sys.stderr.write( "\n")
            sys.stderr.write( "\n")
        else:
            for i in range(M):
                res = []
                for j in range(M):
                    b = self.board[i][j]
                    # print b
                    if b == 0:
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
            # print any(self.can_beat(x, y, direction, player) for direction in Board.dirs)
        if not res:
            return [None]
        return res

    def can_beat(self, x, y, d, player):
        dx, dy = d
        x += dx
        y += dy
        cnt = 0
        # print self.board
        while  0 <= x < M and 0 <= y < M and self.board[y][x] == -player:
            x += dx
            y += dy
            cnt += 1
        return 0 <= x < M and 0 <= y < M and cnt > 0 and self.board[y][x] == player

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
            while  0 <= x < M and 0 <= y < M and self.board[y][x] == -player :
                to_beat.append((x, y))
                x += dx
                y += dy
            if  0 <= x < M and 0 <= y < M and self.board[y][x] == player:
                for (nx, ny) in to_beat:
                    self.board[ny][nx] = player
                    self.revNum[player] += 1
                    self.revNum[-player] -= 1

    def result(self):
        return self.revNum[1] - self.revNum[-1]

    def terminal(self):
        if not self.fields:
            return True
        return self.last_moves[1] == self.last_moves[0] == [None]

    def random_move(self, player):
        ms = self.moves(player)
        # print ms
        if ms and ms != [None]:
            return random.choice(ms)
        return [None]

    def alfabetamove(self, player, depth, my_player):
        ms = self.moves(player)
        # print ms
        if ms and ms != [None]:
            res = []
            for move in ms:
                res.append((alphabeta(nextS(self, move, player),depth, -float('Inf'), float('Inf'), -player, my_player), move))
            # self.draw()
            # print res
            def max_fn(value): return value[0]
            # print max(res, key=max_fn)[1]
            return max(res, key=max_fn)[1]
        return [None]

    def NNMove(self, player):
        ms = self.moves(player)
        # print ms
        if ms and ms != [None]:
            res = []
            for move in ms:
                res.append((val(nextS(self, move, player), player), move))

            def max_fn(value): return value[0]
            return max(res, key=max_fn)[1]
        return [None]


def val(current_state, player):
    if current_state.terminal():
        return float("Inf")
    return NN_value(current_state, player)

def NN_value(state, player):
    ys = nn.predict_proba([addAtributes(boardToTab(state.board))])
    prob_1 = ys[0][0]
    prob1 = ys[0][1]
    if player ==1:
        return prob1
    return prob_1



def alphabeta(state, depth, alpha, beta, player, my_player):
    if state.terminal():
        return float("Inf")
    if depth == 0:
        return heuristic_value(state,-player)

    if player==my_player:
        v = -float("Inf")
        for m in state.moves(player):
            child = nextS(state,m,player)
            v = max(v, alphabeta(child, depth - 1, alpha, beta, -player, my_player))
            alpha = max(alpha, v)
            if beta <= alpha:
                break 
        return v
    else:
        v = float("Inf")
        for m in state.moves(player):
            child = nextS(state,m,player)
            v = min(v, alphabeta(child, depth - 1, alpha, beta, player, my_player))
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v

def nextS(state, move, player):
    nextS = copy.deepcopy(state)
    nextS.do_move(move, player)
    return nextS


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
        if state.board[i][j] == 0:
            for el in cornerDict[(i, j)]:
                (i1, j1) = el
                if state.board[i1][j1] == player:
                    res += 1
                if (i1 == 1 or i1 == 6) and (j1 == 1 or j1 == 6):
                    res += 1
    return res


def heuristic_value(state, player):
    if state.terminal():
        return player * state.result()*float("Inf")
    res = 0
    coin_parity = float(player  *state.result()) / \
        (state.revNum[1]+state.revNum[-1]) # procent pionków

    ending = ((state.revNum[1]+state.revNum[-1])> 55) * coin_parity

    corners_captured = corners(state, player) \
        - corners(state, -player)

    mobility = len(state.moves(player)) \
        - len(state.moves(-player))

    corners_neighbourhood = corners_neighbours(state, player) \
        - corners_neighbours(state, -player)
    
    res += 10 * corners_captured \
        + 1 * mobility \
        - 5 * corners_neighbourhood \
        + 1 * ending
    # state.draw()
    # print "heura: ", res, corners_captured, mobility, corners_neighbourhood, ending, "\n\n"
    return res


def playGame(player, B, my_player):
    while True:
        if player!=my_player:
            m = B.random_move(player)
        else:
            # m = B.alfabetamove(player=player,depth=0, my_player=my_player)
            m = B.NNMove(player=player)
            # m = B.random_move(player)
            
        # print m
        if m and m != None:
            B.do_move(m, player)
        player = -player
        # B.draw(1)
        if B.terminal():
            break

defs = 0
tries = 1000
start_time = time.time()
my_player = 1
for i in range(1, tries+1):
    player = -1
    B = Board()
    playGame(player=player, B=B, my_player=my_player)
    r = B.result()

    if r < 0:
        defs += 1

    if not i % 10:
        print i, ': Result', r, defs
        print("--- %s seconds ---" % (time.time() - start_time))

# print 100 - 100.*defs/tries, "% wygranych"
