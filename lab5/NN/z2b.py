from sklearn.neural_network import MLPClassifier
import pickle

with open('nn_weights.dat') as f:
    nn = pickle.load(f)


row = "______________1_____11_____11______10______001____0_0___________"
temp = []
for i in range(64):
    if row[i] == '_':
        temp += [0]
    elif row[i] == '0':
        temp += [-1]
    elif row[i] == '1':
        temp += [1]
ys = nn.predict_proba([temp])
prob_1 = ys[0][0]
prob1 = ys[0][1]

print "-1" if prob_1> prob1 else "1"

