row = "0010001000"
size = 5

def opt_dist (row, size):
    suma = row.count("1")
    change = len(row)
    index = -1
    for i in range(len(row)-size):
        wind = row[i:i+size]
        _change = size - 2*wind.count("1")+suma
        if _change<change:
            index = i
            change = _change 

    res = [0 for x in range(len(row))]
    res[index:index+size]=[1 for x in range(size)]
    return(res, change)

# test
for x in range(7):
    print(opt_dist(row,x))