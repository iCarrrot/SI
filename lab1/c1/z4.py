S = {}

with open("polish_words.txt") as f:
    for line in f:
        key = line.split()
        S[key[0]] = 1


def df(S, row, dd):
    if not len(row):
        return []
    if row in dd:
        return dd[row]
    else:
        suma = -1
        tense = []
        for i in range(1, len(row)+1):
            if row[:i] in S:
                new_tenses = df(S, row[i:], dd)
                tenses = [row[:i]+x for x in new_tenses]
        dd[row] =tenses
        return tenses

with open("input_1.2.txt") as f:
    for line in f:
        print("".join(x+' ' for x in df(S, line[:-1], {})))

