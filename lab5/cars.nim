const
    #CHANGE EVERYTIME!
    Y = 21
    X = 78

    TRIES = 1000
    REWARD = - 0.1
    GAMMA = 0.99
type 
    dataTuple = tuple[dx,dy:int8,val:float]
    boardType= array[0..TRIES,array[0..Y, array[0..X, array[0..6,array[0..6,dataTuple]]]]]
    tableType = array[0..Y,array[0..X, char]]


# for tr in 0..TRIES:
#     for y in 0..Y:
#         for x in 0..X:
#             for vy in 1..7:
#                 for vx in 1..7:
proc fildChar(inp:char):bool=
    if inp == '#' or inp == 's':
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
        if nx > X:
            nx = X
        if nx < 0:
            nx = 0
        var ny:int = y + nVy - 3
        if ny > Y:
            ny = Y
        if ny < 0:
            ny = 0
               
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
                    board[0][y][x][vy][vx] = (0'i8,0'i8,-100.0)
                elif line[x] == 'e':
                    board[0][y][x][vy][vx] = (0'i8,0'i8,100.0)
                    
for tr in 1..TRIES:
    for y in 0..Y:
        for x in 0..X:
            for vy in 0..6:
                for vx in 0..6:
                    # echo table[y][x]
                    if fildChar(table[y][x]):
                        # echo table[y][x]
                        var 
                            value:float
                            maxValue:dataTuple = (0'i8,0'i8,low(float))
                        for dy in -1'i8..1'i8:
                            for dx in -1'i8..1'i8:
                                # echo dy, " ", dx
                                var (nx, ny, nVx, nVy) = newState(x,y,vx,vy,dx,dy)
                                value = REWARD + GAMMA * board[tr-1][ny][nx][nVy][nVx].val
                                # echo value, " ", maxValue.val
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
                    echo x," ",y," ",vx - 3 ," ",vy - 3,"     ",value.dx," ", value.dy
