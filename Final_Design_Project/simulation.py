#!/usr/bin/env python

import matplotlib.pyplot as plt
import math
import numpy as np

# Nothing = 0, Blue = 1, Green = 2, Yellow = 3, Orange = 4
state = np.array([[0.85, 0.05, 0.05], [0.10, 0.90, 0.10], [0.05, 0.05, 0.85]])
measure = np.array([[0.10, 0.10, 0.10, 0.10], [0.60, 0.20, 0.05, 0.05], [0.20, 0.60, 0.05, 0.05], [0.05, 0.05, 0.65, 0.20], [0.05, 0.05, 0.15, 0.60]])
predict = np.zeros((11,11))
update = np.zeros((11,11))
action = np.array([[1,4],[1,3],[1,2],[1,1],[1,0],[1,2],[1,1],[1,2],[0,4],[1,3],[1,2],[1,1]])
current = np.zeros(11)
clr = np.array([3,2,1,4,4,2,1,4,3,2,1])

# Initialize
for k in range(0,11):
    current[k] = float(1/11)
initial = current

# Localization
for x in range(0,11):
    for k in range(0,11):
        if k + 1 > 10:
            idx = 0
        else:
            idx = k + 1
        predict[x][k] = state[0][action[x][0]+1] * current[idx] + state[1][action[x][0]+1] * current[k] + state[2][action[x][0]+1] * current[k-1]
    for k in range(0,11):
        update[x][k] = measure[action[x][1]][clr[k]-1] * predict[x][k]
    update[x] = update[x]/sum(update[x])
    current = update[x]


# Plot
x = np.array([2,3,4,5,6,7,8,9,10,11,12])
y = update
plt.subplot(6,1,1)
plt.bar(x,initial)
plt.subplot(6,1,2)
plt.bar(x,y[0])
plt.subplot(6,1,3)
plt.bar(x,y[1])
plt.subplot(6,1,4)
plt.bar(x,y[2])
plt.subplot(6,1,5)
plt.bar(x,y[3])
plt.subplot(6,1,6)
plt.bar(x,y[4])
plt.show()

plt.subplot(6,1,1)
plt.bar(x,y[5])
plt.subplot(6,1,2)
plt.bar(x,y[6])
plt.subplot(6,1,3)
plt.bar(x,y[7])
plt.subplot(6,1,4)
plt.bar(x,y[8])
plt.subplot(6,1,5)
plt.bar(x,y[9])
plt.subplot(6,1,6)
plt.bar(x,y[10])
plt.show()
