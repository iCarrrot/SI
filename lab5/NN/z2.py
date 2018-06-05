# coding=utf-8

from sklearn.neural_network import MLPClassifier
import random
import pickle
import numpy as np


def addAtributes(data):
    res = []
    #suma
    res.append(sum(data))
    #rogi
    corners1=0
    corners2=0
    for (i, j) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
        if data[i*8+j] == 1:
            corners1 += 1
        if data[i*8+j] == -1:
            corners2 += 1
    res.append(corners1) 
    res.append(corners2)

    # sąsiedzi rogów
    
    cornerDict = {
        (0, 0): [(1, 0), (0, 1), (1, 1)],
        (0, 7): [(1, 7), (0, 6), (1, 6)],
        (7, 0): [(7, 1), (6, 0), (6, 1)],
        (7, 7): [(7, 6), (6, 7), (6, 6)]
    }
    corners_n1 = 0
    corners_n2 = 0
    for (i, j) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
        if data[i*8+j] == 0:
            for el in cornerDict[(i, j)]:
                (i1, j1) = el
                if data[i1*8+j1] == 1:
                    corners_n1 += 1
                    if (i1 == 1 or i1 == 6) and (j1 == 1 or j1 == 6):
                        corners_n1 += 1
                if data[i1*8+j1] == -1:
                    corners_n2 += 1
                    if (i1 == 1 or i1 == 6) and (j1 == 1 or j1 == 6):
                        corners_n2 += 1

    res.append(corners_n1)
    res.append(corners_n2)

    edge1,edge2 = 0,0
    edge_n1, edge_n2 = 0,0
    for i in range(64):
        x,y = i//8, i%8
        if ((x ==1 or x ==6 ) and 1<=y<=6) or  (( y == 1 or y ==6) and 1<=x<=6):
            if data[i] == 1:
                edge1+=1
            if data[i] ==-1:
                edge2+=1

        if ((x ==2 or x ==5 ) and 2<=y<=5) or  (( y == 2 or y ==5) and 2<=x<=5):
            if data[i] == 1:
                edge_n1+=1
            if data[i] ==-1:
                edge_n2+=1
    res+=[edge1,edge2,edge_n1,edge_n2]
    return res+data



# data: list of pairs (X,y)
# X: vector  of  floats/ints
# y in [v1 ,...,vk]
data = []






with open("reversi_learning_data/bigger.dat") as f:
    for line in f:
        score, row = line.split()
        temp = []
        for i in range(64):
            if row[i] == '_':
                temp += [0]
            elif row[i] == '0':
                temp += [-1]
            elif row[i] == '1':
                temp += [1]

        data += [(addAtributes(temp), int(score)), ]

random.shuffle(data)
N = len(data) / 6

test_data = data[:N]
dev_data = data[N:]
# print test_data

X = [x for (x, _) in dev_data]
y = [i for (x, i) in dev_data]
X_test = [x for (x, _) in test_data]
y_test = [i for (x, i) in test_data]


# creating  model
nn = MLPClassifier(hidden_layer_sizes=(60, 60, 10))
# training  model
print np.array(X).shape, np.array(y).shape
nn.fit(X, y)

print 'Dev  score ', nn.score(X, y)
print 'Test  score ', nn.score(X_test, y_test)

# writing  model
with open('nn_weights_bigger_more.dat', 'w') as f:
    pickle.dump(nn, f)

