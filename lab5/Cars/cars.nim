const
    #CHANGE EVERYTIME!
    
    # z1
    # Y = 11
    # X = 34
    # TRIES = 80

    # z2 & z6
    Y = 21
    X = 78
    TRIES = 800

    #z3
    # Y = 6
    # X = 12
    # TRIES = 80

    #z8 & z9
    # Y = 17
    # X = 64
    # TRIES = 400

    #z10 & z11
    # Y = 16
    # X = 41
    # TRIES = 400

    REWARD = - 0.1
    GAMMA = 0.99
    BAD = -100.0
type 
    dataTuple = tuple[dx,dy:int8,val:float]
    boardType= array[0..TRIES,array[0..Y, array[0..X, array[0..6,array[0..6,dataTuple]]]]]
    tableType = array[0..Y,array[0..X, char]]



proc fildChar(inp:char):bool=
    if inp == '#' or inp == 's' or inp == 'o':
        return true
    return false

proc newState(x:int, y:int, vx:int, vy:int, dx:int8, dy:int8):tuple[nx,ny,nVx,nVy:int8] = 
        var nVx:int = vx + dx
        if nVx > 6:
            nVx = 6
        if nVx < 0:
            nVx = 0
        var nVy:int = vy + dy
        if nVy > 6:
            nVy = 6
        if nVy < 0:
            nVy = 0

        var nx:int = x + nVx - 3
        var ny:int = y + nVy - 3

        return ((int8)nx,(int8)ny,(int8)nVx,(int8)nVy)

# proc printBoard()

var
    line:string
    board : boardType
    table: tableType
for y in 0..Y:
    line = readLine(stdin)
    # echo "r: ", line
    var l = len(line)
    for x in 0..l:
        table[y][x] = line[x]
        for vy in 0..6:
            for vx in 0..6:
                if line[x] == '.':
                    board[0][y][x][vy][vx] = (0'i8,0'i8,BAD)
                elif line[x] == 'e':
                    board[0][y][x][vy][vx] = (0'i8,0'i8,100.0)
                    
for tr in 1..TRIES:
    # echo tr
    for y in 0..Y:
        for x in 0..X:
            for vy in 0..6:
                for vx in 0..6:
                    if fildChar(table[y][x]):
                        var maxValue:dataTuple = (0'i8,0'i8,low(float))
                        for dy in -1'i8..1'i8:
                            for dx in -1'i8..1'i8:
                                # echo dy, " ", dx
                                var 
                                    value:float =0
                                    nx, ny, nVx, nVy:int8
                                if table[y][x] != 'o':
                                    (nx, ny, nVx, nVy) = newState(x,y,vx,vy,dx,dy)                                
                                    if nx<0 or nx>X or ny<0 or ny>Y:
                                        value = REWARD + GAMMA * BAD
                                    else:
                                        value = REWARD + GAMMA * board[tr-1][ny][nx][nVy][nVx].val
                                else:
                                    for rdy in -1'i8..1'i8:
                                        for rdx in -1'i8..1'i8:
                                            (nx, ny, nVx, nVy) = newState(x,y,vx,vy,dx+rdx,dy+rdy)
                                            if nx<0 or nx>X or ny<0 or ny>Y:
                                                value += REWARD + GAMMA * BAD
                                            else:
                                                value += REWARD + GAMMA * board[tr-1][ny][nx][nVy][nVx].val
                                    value = value/9                                        
                                if value > maxValue.val:
                                    maxValue = (dx,dy, value)
                        board[tr][y][x][vy][vx] = maxValue
                    else:
                        board[tr][y][x][vy][vx] = board[tr-1][y][x][vy][vx]


for y in 0..Y:
    for x in 0..X:
        if fildChar(table[y][x]):
            for vy in 0..6:
                for vx in 0..6:
                    var value = board[TRIES][y][x][vy][vx]
                    echo x," ",y," ",vx - 3 ," ",vy - 3,"     ",value.dx," ", value.dy," ", value.val
