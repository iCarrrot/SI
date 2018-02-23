S = {}

with open("polish_words.txt") as f:
    for line in f:
       key= line.split()
       S[key[0]] = 1


def df(S, row, dd):
    if not len(row):
        return (0, [])
    if row in dd:
        return dd[row]
    else:
        suma = -1
        tense = []
        for i in range(1, len(row)+1):
            if row[:i] in S:
                (new_sum, new_tense) = df(S, row[i:], dd)
                if new_sum + i**2 > suma and new_sum > -1:
                     suma = new_sum + i**2
                     tense = [row[:i]]+new_tense
        dd[row]=(suma, tense)
        return (suma, tense)

print(df(S,"tamatematykapustkinieznosi", {})[1])
