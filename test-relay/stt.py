from os import stat
import statistics as stat
import math


l = []
with open('summary.txt', 'r') as f:
    for line in f.readlines():
       l.append(float(line))

mean = stat.mean(l)
pstdev = stat.pstdev(l)

print(str(mean)[:6], str(pstdev)[:6])
