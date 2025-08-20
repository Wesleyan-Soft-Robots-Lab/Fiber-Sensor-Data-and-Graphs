import os
import pandas as pd
import matplotlib.pyplot as plt
dataPath = 'Sensor fiber characterization/5x runs/'
palette = ['#c902e5', '#693FB6','#405AA2','#038185','#008383']

files = ['oldthread_30percent_5x_synced.csv',
         'oldthread_sensorfiber_5x_1_synced.csv',
         'oldthread_sensorfiber_5x_3_synced.csv',
         'oldthread_sensorfiber_5x_4_synced.csv',
         'oldthread_sensorfiber_5x_5_synced.csv',
         'oldthread_sensorfiber_5x_6_synced.csv']

df = pd.read_csv(os.path.join(dataPath,files[4]), header=None)
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
plt.annotate("", xytext=(0, 1), xy=(1, 2.5),
            arrowprops=dict(arrowstyle="->"))
plt.title('Drift Over 5 Loading-Unloading Cycles')
plt.legend()
plt.xlabel('Strain (%)')
plt.ylabel(u'Δ Resistance (%)')
plt.grid()
plt.show()