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
        tenses = []
        for i in range(1, len(row)+1):
            if row[:i] in S:
                new_tenses = df(S, row[i:], dd)
                # print(new_tenses)
                if new_tenses != [] or not len(row[i:]):  
                    if len(new_tenses):
                        tenses += [row[:i]+" "+x for x in new_tenses]
                    else:
                        tenses += [row[:i]]    
        dd[row] =tenses
        return tenses

with open("input_1.2.txt") as f:
    for line in f:
        # print("".join(x+' ' for x in df(S, line[:-1], {})))
        print(df(S,line[:-1],{}))

