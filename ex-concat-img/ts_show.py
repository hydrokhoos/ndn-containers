from matplotlib import pyplot as plt
import pandas as pd


plt.rcParams['figure.autolayout'] = True
plt.rcParams['figure.figsize'] = [6.4, 4.8]
plt.rcParams['font.family'] ='sans-serif'
plt.rcParams['font.size'] = 12
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['xtick.major.width'] = 1.0
plt.rcParams['ytick.major.width'] = 1.0



out = 'ts'

data = pd.read_csv('src/result.csv', header=0, delimiter=',')
data = data.sort_values('time')

out = out + str(data['name'][0]).replace('/', '-')

m = min(data['time'])
data['time'] = (data['time'] - m) * 1000

data.to_csv(out + '.csv')
print(f'CSV saved to [{out}.csv]')

x = data['time'].tolist()
y = data['action'].tolist()

plt.scatter(x, y, c='k', marker='.')

plt.xlabel('time [ms]')
plt.minorticks_on()
plt.grid(which='major', axis='x', color='lightgray', linestyle='solid')
plt.grid(which='minor', axis='x', color='lightgray', linestyle='dotted')

plt.savefig(out)
print(f'Figure saved to [{out}.png]')
