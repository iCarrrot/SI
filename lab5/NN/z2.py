from sklearn.neural_network import MLPClassifier
import random
import pickle
# data: list of pairs (X,y)
# X: vector  of  floats/ints
# y in [v1 ,...,vk]
data = []
with open("reversi_learning_data/smaller.dat") as f:
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
        data += [(temp, [int(score)]), ]

print data[0]
print data[1]
random.shuffle(data)
N = len(data) / 6
test_data = data[:N]
dev_data = data[N:]
X = [x for (x, y) in dev_data]
y = [y for (x, y) in dev_data]
X_test = [x for (x, y) in test_data]
y_test = [y for (x, y) in dev_data]

# creating  model
nn = MLPClassifier(hidden_layer_sizes=(60, 60, 10))
# training  model
nn.fit(X, y)

print 'Dev  score ', nn.score(X, y)
print 'Test  score ', nn.score(X_test, y_test)

# writing  model
with open('nn_weights.dat', 'w') as f:
    pickle.dump(nn, f)

# from sklearn.neural_network import MLPClassifier
# import pickle
# with open('nn_weights.dat') as f:
#     nn = pickle.load(open(f))

# x = data_vector
# probabilities = nn.predict_proba([x])
# prob0 = ys[0][0]
# prob1 = ys[0][1]
