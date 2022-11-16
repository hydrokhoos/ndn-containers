import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Segment size: 4.4KB
SEG_SIZE = 4.4

plt.rcParams['figure.autolayout'] = True
plt.rcParams['figure.figsize'] = [6.4, 4.8]
plt.rcParams['font.family'] ='sans-serif'
plt.rcParams['font.size'] = 12
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['xtick.major.width'] = 1.0
plt.rcParams['ytick.major.width'] = 1.0
markers = ['o', '^', 's', 'p', 'h', 'D']


# files = ['nonrelay.csv', 'relay-w-q.csv']
# files = ['relay-wo-q.csv', 'relay-w-q.csv']
files = ['multi' + str(i) + '.csv' for i in range(1, 5)]
files = ['segment_fetcher.csv'] + files
fig = ''
for file in files:
    fig += str(file).replace('.csv', '') + '--'
fig = fig[:-2]
# fig += '(seg)'
fig += '.png'

for i, file in enumerate(files):
    df = pd.read_csv(file, header=0, delimiter=',')
    plt.scatter(x=df['data size'].tolist(),
    # plt.scatter(x=[(x+SEG_SIZE-1)//SEG_SIZE for x in df['data size'].tolist()],
                y=df['consumer get time'].tolist(),
                c='white',
                edgecolors='black',
                marker=markers[i],
                label=str(file).replace('.csv', ''))

plt.xlabel('data size [KB]')
# plt.xlabel('number of segments')
plt.ylabel('consumer get time [s]')
plt.legend()

plt.savefig(fig)
print(f'Saved [{fig}]')
