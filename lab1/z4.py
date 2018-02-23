row = "0010001000"
row = [int(x) for x in row]
# size = 5


def opt_dist(row, size):
    suma = sum(row)
    change = len(row)
    index = -1
    for i in range(len(row)-size+1):
        wind = row[i:i+size]
        _change = size - 2*sum(wind) + suma
        if _change < change:
            index = i
            change = _change

    res = [0 for x in range(len(row))]
    res[index:index+size] = [1 for x in range(size)]
    return(res, change)


# test
if __name__ == "__main__":
    opt_dist(row,10)
    for x in range(len(row)+1):
        print(opt_dist(row, x))
