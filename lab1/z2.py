S = {
    "ta": 1,
    "matematyka": 1,
    "pustki": 1,
    "nie": 1,
    "znosi": 1,
    "tama": 1,
    "tematy": 1,
    "kapustki": 1,
    "nie": 1,
    "z": 1,
    "nosi": 1
}

# TODO końcówka nie działą 
def df(S, row, dd):
    if not len(row):
        return (0, [])
    if row in dd:
        return dd[row]
    else:
        sum_ = 0
        tense = []
        for i in range(1, len(row)):
            if row[:i] in S:
                (_sum_, _tense) = df(S, row[i:], dd)
                if _sum_ + i**2 > sum_:
                     sum_ = _sum_ + i**2
                     tense = [row[:i]]+_tense
        dd[row]=(sum_, tense)
        return (sum_, tense)
print(df(S,"tamatematykapustkinieznosi", {}))