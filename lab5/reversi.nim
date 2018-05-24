import random
import times
import strutils
import math
import os

const
    M = 8'i8
    DIRS = [(0'i8, 1'i8), (1'i8, 0'i8), (-1'i8, 0'i8), (0'i8, -1'i8),(1'i8, 1'i8), (-1'i8, -1'i8), (1'i8, -1'i8), (-1'i8, 1'i8)]
    DEPTH = 0
type
    row = array[0'i8..M-1, int8]
    boardT = array[0'i8..M-1, row]
    moveT = tuple[x,y:int8]
    playerT = int8


proc initial_board(): boardT =
    var B : boardT
    for i in 0..M-1:
        for j in 1..M-1:
            B[i][j] = 0
    B[3][3] = 1
    B[4][4] = 1
    B[3][4] = -1
    B[4][3] = -1
    return B


type
    Board =  ref object of RootObj
        board: boardT
        last_moves : tuple[l1,l2:moveT]
        revNum : tuple[p0,p1:int8]
    

method init(this: Board) = 
    this.board = initial_board()
    this.last_moves = ((-100'i8,-100'i8),(-100'i8,-100'i8))
    this.revNum = (2'i8, 2'i8)

method copy(this:Board, that:Board) =
    this.board = that.board
    this.last_moves = that.last_moves
    this.revNum = that.revNum



method can_beat(self:Board, gx:int8, gy:int8, d:moveT, player:playerT):bool =
    var 
        dx,dy:int8
        cnt: int8
        x,y:int8
    (x,y) = (gx,gy) 
    (dx,dy) = (d.x,d.y)
    x += dx
    y += dy
    cnt = 0
    # print self.board
    while  0 <= x and x < M and 0 <= y and y < M and self.board[y][x] == -player:
        x += dx
        y += dy
        cnt += 1
    return 0 <= x and x < M and 0 <= y and y < M and cnt > 0 and self.board[y][x] == player

iterator moves(self:Board, player:playerT):moveT=
    for y in 0'i8..M-1:
        for x in 0'i8..M-1:            
            if self.board[y][x] == 0:
                var check = 0
                for k,direction in DIRS:
                    if self.can_beat(x, y, direction, player):
                        check += 1
                        break
                if check>0:
                    var a:moveT = (x,y)
                    yield a

method do_move(self:Board, move:moveT, player:playerT) =
    self.last_moves = (self.last_moves.l2, move)
    # print move
    if move != (-1'i8,-1'i8):
        var 
            x,y,x0,y0:int8
            it :int8 = 0'i8
        (x, y) = move
        (x0, y0) = move
        self.board[y][x] = player
        if player == 1:
            self.revNum.p1 += 1
        else:
            self.revNum.p0 += 1
        for k,v in DIRS:
            (x, y) = (x0, y0)
            var dx,dy:int8
            (dx,dy) = v
            x += dx
            y += dy
            var to_beat:seq[moveT] = @[]
            while  0 <= x and x < M and 0 <= y and y  < M and self.board[y][x] == -player :
                to_beat.add((x, y))
                x += dx
                y += dy
                it+=1
            if  0 <= x and x< M and 0 <= y and y < M and self.board[y][x] == player:
                for k,v in to_beat:
                    var nx,ny:int8
                    (nx, ny) = v
                    if nx != -1 and ny != -1:
                        self.board[ny][nx] = player
                        if player == 1:
                            self.revNum.p1 += 1
                            self.revNum.p0 -= 1
                        else:
                            self.revNum.p1 -= 1
                            self.revNum.p0 += 1
                            
method result(self:Board):int8 = 
    return self.revNum.p1 - self.revNum.p0

method terminal(self:Board):bool = 
    if self.revNum.p0+self.revNum.p1 == 64:
        return true
    
    return self.last_moves[1] == self.last_moves[0] and self.last_moves[1] == (-1'i8,-1'i8)

method random_move(self:Board, player:playerT):moveT=
    var moves: seq[moveT] = @[]
    for s in self.moves(player):
      moves.add(s)
    if len(moves) == 0:
        return (-1'i8,-1'i8)
    return moves.rand()



proc nextS(state:Board, move:moveT, player:playerT):Board = 
    var nextS =Board() 
    nextS.copy(state)
    nextS.do_move(move, player)
    return nextS



proc corners(state:Board, player:playerT):int8=
    var res:int8 = 0
    for k,v in [(0, 0), (0, 7), (7, 0), (7, 7)]:
        var (i, j) = v 
        if state.board[i][j] == player:
            res += 1
    return res


proc corners_neighbours(state:Board, player:playerT):int8=
    var res:int8 = 0
    var cornerDict = [
        [(1, 0), (0, 1), (1, 1)],
        [(1, 7), (0, 6), (1, 6)],
        [(7, 1), (6, 0), (6, 1)],
        [(7, 6), (6, 7), (6, 6)]
    ]
    # echo 3
    var corners = [(0, 0,0), (1,0, 7), (2,7, 0), (3,7, 7)] 
    for b in 0..3 :
        var (number, i, j) = corners[b]
        if state.board[i][j] == 0:
            for a in 0..2:
                var v1 = cornerDict[number][a]
                var (i1, j1) = v1
                if state.board[i1][j1] == player:
                    res += 1
                
                if (i1 == 1 or i1 == 6) and (j1 == 1 or j1 == 6):
                    res += 1
                
    return res


proc heuristic_value(state:Board, player:playerT):float=
    # echo 11    
    if state.terminal():
        return (float)(player * state.result()) * high(float)
    var coin_parity = float(player * state.result()) / (float)(state.revNum[1]+state.revNum[0]) # procent pionków

    var ending = (float)((state.revNum[1]+state.revNum[0])> 55) * coin_parity

    var corners_captured = corners(state, player) - corners(state, -player)
    # echo 10    
    var moves1: seq[moveT] = @[]
    var moves2: seq[moveT] = @[]
    for s in state.moves(player):
      moves1.add(s)
    for s in state.moves(-player):
      moves2.add(s)
    var mobility = len(moves1) - len(moves2)
    # echo 14
    
    var corners_neighbourhood = corners_neighbours(state, player) - corners_neighbours(state, -player)
    # echo 15
    
    var res = (float)(10 * corners_captured + 1 * mobility - 5 * corners_neighbourhood )+ 1 * ending
    # state.draw()
    # print "heura: ", res, corners_captured, mobility, corners_neighbourhood, ending, "\n\n"
    # echo 10
    
    return res

proc alphabeta(state:Board, depth:int8, alpha:float, beta:float, player:playerT, my_player:playerT):float = 
    if state.terminal():
        return high(float)
    if depth == 0:
        return heuristic_value(state,-player)
    # echo 10
    if player==my_player:
        var v = low(float)
        for m in state.moves(player):
            var child = nextS(state,m,player)
            v = max(v, alphabeta(child, depth - 1, alpha, beta, -player, my_player))
            var alpha = max(alpha, v)
            if beta <= alpha:
                break 
        return v
    else:
        var v = high(float)
        for m in state.moves(player):
            var child = nextS(state,m,player)
            v = min(v, alphabeta(child, depth - 1, alpha, beta, player, my_player))
            var beta = min(beta, v)
            if beta <= alpha:
                break
        return v

method alphabetamove(self:Board, player:playerT, depth:int8, my_player:playerT):moveT = 
    var 
    # print ms
        bestM:moveT = (-1'i8,-1'i8)
        max = low(float)

    for move in self.moves(player):
        # echo move
        var v = alphabeta(nextS(self, move, player),depth, low(float), high(float), -player, my_player)
        if v > max:
            max = v
            bestM = move

    return bestM
  




proc playGame(gplayer:playerT, B:Board, my_player:playerT)=
    var player = gplayer
    randomize()
    while true:
        # echo "1"
        var m:moveT
        if player!=my_player:
            # echo "3"
            m = B.random_move(player)
            # echo "4"
        else:
            # echo "5"
            m = B.alphabetamove(player,DEPTH, my_player)
            # echo "6"
            # m = B.random_move(player)
        # print m
        # echo "1"
        B.do_move(m, player)
        player = -player
        # B.draw(1)
        if B.terminal():
            break
        # echo m


var 
    defs:float = 0
    tries = 1000
    start_time = cpuTime()
    my_player = 1'i8
    player = -1'i8
    B = Board()

for i in 1..tries+1:
    # echo "1"
    B = Board()
    B.init()
    playGame(player, B, my_player)
    var r = B.result()
    # echo r
    if r < 0:
        defs += 1
    if (i %% 50) == 0:
        echo "$1: Result $2 (przegranych: $3)" % [$i,$r,$defs]
        let time = cpuTime() - start_time
        echo "--- $1 seconds ---" % [$time]

echo 100.0 - 100.0*defs/(float)tries , "% wygranych"
    