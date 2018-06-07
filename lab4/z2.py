# -*- coding: utf-8
import random
import sys
from collections import defaultdict as dd
import copy


BOK = 30
SX = -100
SY = 0
M = 7
N = 9
water = {
    (1, 3), (2, 3), (4, 3), (5, 3),
    (1, 4), (2, 4), (4, 4), (5, 4),
    (1, 5), (2, 5), (4, 5), (5, 5)
}

traps = {(2, 0), (4, 0), (3, 1), (2, 8), (4, 8), (3, 7)}
goal = {0: (3, 8), 1: (3, 0)}
animalSet = {"L", "T", "D", "C", "R", "J", "W", "E"}
animalDict = {"R": 1, "C": 2, "D": 3, "W": 4, "J": 5, "T": 6, "L": 7, "E": 8}
reverseAnimalDict = {1: "R", 2: "C", 3: "D",
                     4: "W", 5: "J", 6: "T", 7: "L", 8: "E"}
# player 1 = uppercase, player 0 = lowercase

###################################


def change(fig, player, first_player):
    x = fig.upper() if player != first_player else fig.lower()
    return x


def initial_board():
    T = [
        "..#*#..",
        "...#...",
        ".......",
        ".~~.~~.",
        ".~~.~~.",
        ".~~.~~.",
        ".......",
        "...#...",
        "..#*#..",
    ]
    F = [
        "L.....T",
        ".D...C.",
        "R.J.W.E",
        ".......",
        ".......",
        ".......",
        "e.w.j.r",
        ".d...c.",
        "t.....l",
    ]
    B = [["."] * 7 for _ in range(9)]
    Terrain = [["."] * 7 for _ in range(9)]
    animals = dict()
    for i in range(9):
        # x=""
        for j in range(7):
            Terrain[i][j] = T[i][j]
            if B[i][j] == '.':
                B[i][j] = T[i][j]
            if B[i][j] == '.':
                B[i][j] = F[i][j]
            if F[i][j] != '.':
                animals[F[i][j]] = (j, i)
            # x+=B[i][j]
        # print x, "\n"
    # print animals
    return B, animals, Terrain


initial_board()


class Board:
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    def __init__(self, fromBoard=None, empty=True):
        if not empty:
            self.board = copy.deepcopy(fromBoard.board)
            self.animalsCoords = fromBoard.animalsCoords.copy()
            # print "\ninit:\n", self.animalsCoords,"\n", fromBoard.animalsCoords
            self.Terrain = copy.deepcopy(fromBoard.Terrain)
            # print self.animalsCoords
            self.move_list = copy.deepcopy(fromBoard.move_list)
            self.history = copy.deepcopy(fromBoard.history)
            self.pacifistMoves = copy.deepcopy(fromBoard.pacifistMoves)
            self.ifWin = copy.deepcopy(fromBoard.ifWin)

        else:
            self.board, self.animalsCoords, self.Terrain = initial_board()
            # print self.animalsCoords
            self.move_list = []
            self.history = []
            self.pacifistMoves = 0
            self.ifWin = False

    def draw(self):
        for i in range(N):
            res = []
            for j in range(M):
                b = self.board[i][j]
                res.append(b)

            # print ''.join(res)
        # print

    def moves(self, player, first_player):
        res = []
        for c in animalSet:
            # print self.animalsCoords[c], self.animalsCoords[c.lower()], c, c.lower()
            (x, y) = self.animalsCoords[c] if player != first_player \
                else self.animalsCoords[c.lower()]
            # print (x, y), player, c
            if x != None and y != None:
                # print c
                res += self.check(player, (x, y), c, first_player)
        if not res:
            return [None]
        return res

    def check(self, player, coords, typ, first_player):
        (x, y) = coords
        moves = []
        for dx, dy in self.dirs:
            x1, y1 = x - dx, y-dy
            if x1 >= 0 and y1 >= 0 and x1 < 7 and y1 < 9:
                fig = self.board[y1][x1]
                if typ == "T" or typ == "L":
                    while fig == '~':
                        # print x1, y1, fig, typ
                        x1, y1 = x1 - dx, y1-dy
                        fig = self.board[y1][x1]

                    if fig != '~' and (x1, y1) in water:
                        continue

                if fig == '.'  \
                        or fig == '#' \
                        or (fig == '*' and goal[player] == (x1, y1)) \
                        or (typ == "R" and fig == '~'):

                    moves += [(change(typ, player, first_player), x1, y1)]

                elif fig.isalpha() \
                        and ((player != first_player and not fig.istitle()) or (not player != first_player and fig.istitle())) \
                        and (x, y) not in water \
                        and (typ == "R" or (x1, y1) not in water):
                    moves += self.can_beat(typ, fig,
                                           (x1, y1), player, first_player)
        return moves

    def can_beat(self, fig1, fig2, coords, player, first_player):
        """
        Arguments:
            fig1 {char} -- figura bijaca
            fig2 {char} -- figura bita
            coords {(int,int)} -- wspolrzedne figuty bitej

        Returns:
            [(int,int)] -- wspolrzedne lub None
        """

        (x, y) = coords
        if (x, y) in traps \
                or (fig1.upper() == 'R' and fig2.upper() == 'E')\
                or animalDict[fig1.upper()] >= animalDict[fig2.upper()]:
            # print fig1, animalDict[fig1.upper()], fig2, animalDict[fig2.upper()]
            return [(change(fig1, player, first_player), x, y)]
        return []

    def get(self, x, y):
        if 0 <= x < M and 0 <= y < N:
            return self.board[y][x]
        return None

    def do_move(self, move, player, first_player):
        self.history.append([x[:] for x in self.board])
        self.move_list.append(move)

        if move == None:
            return
        fig, x, y = move
        lastX, lastY = self.animalsCoords[fig]
        # print self.animalsCoords
        # if lastX ==None or lastY == None:

        #     print fig, x,y,lastX, lastY, self.animalsCoords
        #     self.draw()
        self.animalsCoords[fig] = (x, y)
        newFiled = self.board[y][x]

        self.board[y][x] = fig
        self.board[lastY][lastX] = self.Terrain[lastY][lastX]
        self.animalsCoords[fig] = (x, y)
        self.pacifistMoves += 1
        if newFiled.upper() in animalSet:
            self.pacifistMoves = 0
            self.animalsCoords[newFiled] = (None, None)
        elif goal[player] == (x, y):
            # self.draw()
            # print player, goal[player], x, y, fig, newFiled
            # raise Exception("Game Over, player "+player+" won")
            self.ifWin = True

    def result(self, player, first_player):
        if self.ifWin:
            return (True, player)
        if self.pacifistMoves >= 50:
            # print "to skomplikowane"
            for i in range(8, 0, -1):
                c = reverseAnimalDict[i]
                if self.animalsCoords[c] == (None, None) and self.animalsCoords[c.lower()] != (None, None):
                    # print 1, i
                    return (True, 0)
                if self.animalsCoords[c] != (None, None) and self.animalsCoords[c.lower()] == (None, None):
                    # print 2, i
                    return (True, 1)

            for i in range(8, 0, -1):
                c = reverseAnimalDict[i]
                if self.animalsCoords[c] != (None, None):
                    (x, y) = self.animalsCoords[c.lower()]
                    (x1, y1) = self.animalsCoords[c]
                    dist = abs(goal[0][0] - x) + abs(goal[0][1] - y)
                    dist1 = abs(goal[1][0] - x1) + abs(goal[1][1] - y1)
                    if dist1 == dist:
                        continue
                    else:
                        # print 3, i, dist, dist1
                        return (True, int(dist1 < dist))
            # print 4
            return (True, 1)
        return (False, player)

    def random_move(self, player, first_player):
        ms = self.moves(player, first_player)
        # print ms
        if ms:
            return random.choice(ms)
        return [None]


def randomPlay(board, player):
    steps = 0
    while True:
        m = board.random_move(player, first_player)
        board.do_move(m, player, first_player)
        res, wp = board.result(player, first_player)
        steps += 1
        if res:
            return wp, steps
        player = 1-player


def randomAgent(board, player, LEN, first_player):
    moves = board.moves(player, first_player)
    results = {i: 0 for i in range(len(moves))}
    steps, i = 0, 0
    while steps < LEN:
        newboard = Board(fromBoard=board, empty=False)
        newboard.do_move(moves[i], player, first_player)
        player2 = 1-player
        wp, step = randomPlay(newboard, player2)
        results[i] += 1 if wp == player else -1
        steps += step+50
        i = (i+1) % len(moves)

    best = max([(v, k) for k, v in results.items()])
    return moves[best[1]]


def heuristic(board, player, first_player):
    #TODO heurystyka wchodzi do własnej jamy
    value = 0
    minTax = 10000
    for c in animalSet:
        # suma po zwierzętach, a potem (10-min(tax) )*4
        c = c if player != first_player else c.lower()
        c1 = change(c, 1-player, first_player)
        # print c, c1
        (x, y) = board.animalsCoords[c]
        (x1, y1) = board.animalsCoords[c1]
        if x != None and y != None:
            value += animalDict[c.upper()]
        if x1 != None and y1 != None:
            value -= animalDict[c1.upper()]

        if x != None and y != None:
            dist = abs(goal[player][0] - x) + abs(goal[player][1] - y)
            # dist1 = abs(goal[1-player][0] - x1) + abs(goal[1-player][1] - y1)
            # print c.upper(), animalDict[c.upper()], dist
            # value += dist*(10-animalDict[c.upper()])
            if dist < minTax:
                minTax = dist
    value += (10-minTax)*4
    # print value

    return value


def betterAgent(board, player, first_player):
    moves = board.moves(player, first_player)
    results = {i: 0 for i in range(len(moves))}
    for i in range(len(moves)):
        newboard = Board(fromBoard=board, empty=False)
        newboard.do_move(moves[i], player, first_player)
        value = heuristic(newboard, player, first_player)

        results[i] += value
    # print results,"\n", moves
    best = max([(v, k) for k, v in results.items()])
    return moves[best[1]]


winner = 0
tries = 10
first_player = 1
B = Board()
games =0
# for _ in range(tries):
#     first_player = 1
#     player = 0
#     B = Board()

#     while True:
#         # B.draw()
#         if not (player != first_player):
#             m = randomAgent(B, player, 2000, first_player)
#         else:
#             # m = B.random_move(player)
#             m = betterAgent(B, player, first_player)
#         if m == None:
#             wp = 1-player
#             break

#         print m, B.pacifistMoves
#         # raw_input()
#         B.do_move(m, player, first_player)

#         res, wp = B.result(player, first_player)
#         if res:
#             break
#         player = 1-player

#         # raw_input()
#         # if B.terminal():
#         #     break

#     winner += 1 if wp == first_player else 0
#     B.draw()
#     first_player = 1-first_player
#     print 'player ', int(wp == 1-first_player), ' won '
# print winner*100. / tries, "%"
# # raw_input('Game over!')
my_player =-1
print "RDY"
while True:
    line = sys.stdin.readline().split()
    cmd, args = line[0], line[1:]
    if cmd == "HEDID":
        if my_player == -1:
            my_player = 1-first_player
        move = tuple(int(x) for x in args[2:])

        if move[0] >= 0 and move[1] >= 0:
            fig = B.get(move[0], move[1])
            # print move, fig
            move = (fig, move[2], move[3])
            B.do_move(move, 1-my_player, first_player)

        m = betterAgent(B, my_player, first_player)
        if m and m != [None]:
            figCoords = B.animalsCoords[m[0]]
            B.do_move(m, my_player, first_player)
            # print figCoords, m
            
            print "IDO", figCoords[0], figCoords[1], m[1], m[2]
        else:
            print "IDO -1 -1 -1 -1"

    elif cmd == "UGO":
        if my_player == -1:
            my_player = first_player

        m = betterAgent(B, my_player, first_player)
        if m and m != [None]:
            figCoords = B.animalsCoords[m[0]]
            B.do_move(m, my_player, first_player)
            
            # print figCoords, m
            print "IDO", figCoords[0], figCoords[1], m[1], m[2]
        else:
            print "IDO -1 -1 -1 -1"
    elif cmd == "ONEMORE":
        B = Board()
        my_player = -1
        games += 1
        sys.stderr.write(str(games)+"\n")

        print "RDY"
    elif cmd == "BYE":
        break
    # B.draw()

# sys.exit(0)
