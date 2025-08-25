import os
import pandas as pd
import matplotlib.pyplot as plt

dataPath = 'Sensor fiber characterization/5x runs/'

palette = ['#c902e5', '#693FB6','#405AA2','#038185','#008383']

file = 'oldthread_sensorfiber_5x_5_synced.csv'

df = pd.read_csv(os.path.join(dataPath,file), header=None)
df['res_change'] = (df[3] - df[3][0])*(df[3][0]**-1) *100 #(Ri − R0) · (R0)^−1
x = 30*df[1]/df[1].max() #scale to 30

#valleys /\,/\,/\,/\,/\
valleys = df.index[(df[1].shift(1)>= df[1]) & (df[1]< df[1].shift(-1))].to_list()
df['color'] = 0
df.loc[valleys[0]:valleys[1], 'color'] = 1
df.loc[valleys[1]:valleys[2], 'color'] = 2
df.loc[valleys[2]:valleys[3], 'color'] = 3
df.loc[valleys[3]:, 'color'] = 4
for c in df['color'].unique():
    cycle = df[df['color'] == c]
    plt.plot(x[cycle.index], cycle['res_change'], color=palette[c], label=f' cycle {c+1}')

# Plot design
plt.annotate("", xytext=(0, 1), xy=(1, 2.5), arrowprops=dict(arrowstyle="->"))
plt.title('Drift Over 5 Loading-Unloading Cycles',fontsize=20)
plt.legend()
plt.xlabel('Strain (%)',fontsize=15)
plt.ylabel(u'Δ Resistance (%)',fontsize=15)
plt.grid()
plt.show()