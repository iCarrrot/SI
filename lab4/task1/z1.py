import random
import sys
from collections import defaultdict as dd
# from turtle import *

#####################################################
# turtle graphic
#####################################################
# tracer(0, 1)

BOK = 30
SX = -100
SY = 0
M = 8


# def kwadrat(x, y, kolor):
#     fillcolor(kolor)
#     pu()
#     goto(SX + x * BOK, SY + y * BOK)
#     pd()
#     begin_fill()
#     for i in range(4):
#         fd(BOK)
#         rt(90)
#     end_fill()


# def kolko(x, y, kolor):
#     fillcolor(kolor)

#     pu()
#     goto(SX + x * BOK + BOK/2, SY + y * BOK - BOK)
#     pd()
#     begin_fill()
#     circle(BOK/2)
#     end_fill()

#####################################################


def initial_board():
    B = [[None] * M for _ in range(M)]
    B[3][3] = 1
    B[4][4] = 1
    B[3][4] = 0
    B[4][3] = 0
    return B

def playGame(player, B, isRandom):
    while True:
        if isRandom:
            m = B.random_move(player)
            B.do_move(m, player)
            player = 1-player
            # raw_input()
            if B.terminal():
                break
        else:
            if not player:
                m = B.random_move(player)
                B.do_move(m, player)
                player = 1-player
                # raw_input()
                if B.terminal():
                    break
            else:
                # m = B.greedy_move(player)
                m = B.semi_random_move(player, 100)
                print m
                B.do_move(m, player)
                player = 1-player
                # raw_input()
                if B.terminal():
                    break

class Board:
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def __init__(self, *args):
        if len(args)>0 and type(args[0]) == type(dict()):
            initialDict = args[0]
            self.board = initialDict["board"]
            self.fields = initialDict["fields"]
            self.move_list = initialDict["move_list"]
            self.history = initialDict["history"]
            
        else:
            self.board = initial_board()
            self.fields = set()
            self.move_list = []
            self.history = []
            for i in range(M):
                for j in range(M):
                    if self.board[i][j] == None:   
                        self.fields.add( (j,i) )
                                        

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

    # def show(self):
    #     for i in range(M):
    #         for j in range(M):
    #             kwadrat(j, i, 'green')

    #     for i in range(M):
    #         for j in range(M):
    #             if self.board[i][j] == 1:
    #                 kolko(j, 7-i, 'black')
    #             if self.board[i][j] == 0:
    #                 kolko(j, 7-i, 'white')

    def moves(self, player):
        res = []
        for (x, y) in self.fields:
            count = 0
            for direction in Board.dirs:
                isOk, cnt = self.can_beat(x, y, direction, player)
                if isOk:
                    count += cnt
            if count > 0:
                res.append(((x, y), count), )
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
        return cnt > 0 and self.get(x, y) == player, cnt

    def get(self, x, y):
        if 0 <= x < M and 0 <= y < M:
            return self.board[y][x]
        return None

    def do_move(self, move, player):
        self.history.append([x[:] for x in self.board])
        self.move_list.append(move)

        if move == [None] or move == None:
            return
        x, y = move
        x0, y0 = move
        self.board[y][x] = player
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

    def result(self):
        res = 0
        for y in range(M):
            for x in range(M):
                b = self.board[y][x]
                if b == 0:
                    res -= 1
                elif b == 1:
                    res += 1
        return res

    def terminal(self):
        if not self.fields:
            return True
        if len(self.move_list) < 2:
            return False
        return self.move_list[-1] == self.move_list[-2] == [None]

    def random_move(self, player):
        ms = self.moves(player)
        # print ms
        if ms and ms != [None]:
            return random.choice(ms)[0]
        return [None]

    def greedy_move(self, player):
        ms = self.moves(player)
        # print player, ms
        if ms!= [None] and ms:
            _max, bestM = 0, tuple()
            for (m,cnt) in ms:
                if cnt > _max:
                    _max, bestM = cnt, m 
            return bestM
        return [None]

    def semi_random_move(self, player, tries):
        ms = self.moves(player)
        # print player, ms
        if ms!= [None] and ms:
            _max, bestM = -1, tuple()
            for (m,_) in ms:
                initialDict = {
                    "board" : self.board,
                    "fields": self.fields,
                    "move_list":self.move_list,
                    "history": self.history,
                }
                wins = 0
                for i in range(tries):
                    tempBoard = Board(initialDict)
                    tempBoard.do_move(m,player)
                    player = 1-player
                    playGame(player=player, B=tempBoard, isRandom=True)
                    r = tempBoard.result()
                    if r>0:
                        wins+=1
                moveRatio = 100.*wins/i
                if moveRatio > _max:
                    _max = moveRatio
                    bestM = m
            return bestM
        return [None]

win = 0
tries = 100

for i in range(tries):
    player = 0
    B = Board()
    playGame(player=player, B=B, isRandom=False)

    # B.draw()
    # B.show()
    r = B.result()
    print i, ': Result', r
    if r > 0:
        win+=1
    # raw_input('Game over!')


    # sys.exit(0)
print 100.*win/tries, "% wygranych"