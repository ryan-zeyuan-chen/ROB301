#!/usr/bin/env python

import matplotlib.pyplot as plt
import math
import numpy as np

# Nothing = 0, Blue = 1, Green = 2, Yellow = 3, Orange = 4
state = [[0.85, 0.05, 0.05], [0.10, 0.90, 0.10], [0.05, 0.05, 0.85]]
measure = [[0.10, 0.10, 0.10, 0.10], [0.60, 0.20, 0.05, 0.05], [0.20, 0.60, 0.05, 0.05], [0.05, 0.05, 0.65, 0.20], [0.05, 0.05, 0.15, 0.60]]
predict = []
update = []
action = [[1,4],[1,3],[1,2],[1,1],[1,0],[1,2],[1,1],[1,2],[0,4],[1,3],[1,2],[1,1]]
current = []
map = [3,2,1,4,4,2,1,4,3,2,1]

# Initialize
for k in range(0,11):
    current.append(0.0)
    current[k] = float(1/11)

# Localization
for x in range(0,11):
    idk = 0
    sum = 0.0
    predict.append([])
    update.append([])
    for k in range(0,11):
        predict[x].append(0.0)
        update[x].append(0.0)
        if k + 1 > 10:
            idx = 0
        else:
            idx = k + 1
        predict[x][k] = predict[x][k] + state[0][action[x][0]+1] * current[k-1]
        predict[x][k] = predict[x][k] + state[1][action[x][0]+1] * current[k]
        predict[x][k] = predict[x][k] + state[2][action[x][0]+1] * current[idx]
        for j in range(0,4):
            if map[k] == j+1:
                sum = sum + measure[action[x][1]][j] * predict[x][k]
                update[x][k] = measure[action[x][1]][j] * predict[x][k]
    for k in range(0,11):
        update[x][k] = update[x][k]/sum
    current = update[x]

# Plot
x = np.array([2,3,4,5,6,7,8,9,10,11,12])
y = np.array(update)
plt.subplot(6,1,1)
plt.bar(x,y[0])
plt.subplot(6,1,2)
plt.bar(x,y[1])
plt.subplot(6,1,3)
plt.bar(x,y[2])
plt.subplot(6,1,4)
plt.bar(x,y[3])
plt.subplot(6,1,5)
plt.bar(x,y[4])
plt.subplot(6,1,6)
plt.bar(x,y[5])
plt.show()

plt.subplot(5,1,1)
plt.bar(x,y[6])
plt.subplot(5,1,2)
plt.bar(x,y[7])
plt.subplot(5,1,3)
plt.bar(x,y[8])
plt.subplot(5,1,4)
plt.bar(x,y[9])
plt.subplot(5,1,5)
plt.bar(x,y[10])
plt.show()
