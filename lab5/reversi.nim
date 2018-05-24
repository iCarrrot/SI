import sets

iterator countTo(n: int): int =
    var i = 0
    while i <= n:
      yield i
      inc i

const
    BOK = 30
    SX = -100
    SY = 0
    M = 8

type
    row = array[0..M, int]
    boardT = array[0..M, row]



proc initial_board(): boardT =
    var B : boardT
    for i in 1..M:
        for j in 1..M:
            B[i][j] = -1
    B[3][3] = 1
    B[4][4] = 1
    B[3][4] = 0
    B[4][3] = 0
    return B


type
    Board =  ref object of RootObj
        dirs*: array[8,tuple[a, b: int]]
        board: boardT
        test:int

method init(this: Board) = 
    this.test = 100
    this.board = initial_board()

method copy(this:Board, that:Board) =
    this.test = that.test
    this.board = that.board

var x = initial_board()
var y = x
echo y[3][3], " ",x[3][5]
x[3][3] = 10
echo y[3][3]," ", x[3][3]




