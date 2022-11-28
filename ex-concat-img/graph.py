import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams['figure.autolayout'] = True
plt.rcParams['figure.figsize'] = [6.4, 4.8]
plt.rcParams['font.family'] ='sans-serif'
plt.rcParams['font.size'] = 12
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['xtick.major.width'] = 1.0
plt.rcParams['ytick.major.width'] = 1.0


file = 'cgettime.csv'
fig = file.replace('.csv', '.png')

data = pd.read_csv(file, header=0, delimiter=',')
print(data)
x = data['data size'].tolist()
y = data['consumer get time'].tolist()

plt.scatter(x, y, c='white', edgecolors='black', marker='o',)

plt.xlabel('data size [KB]')
plt.ylabel('consumer get time [s]')


plt.savefig(fig)

exit()
