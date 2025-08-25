import os
import pandas as pd
import matplotlib.pyplot as plt
dataPath = 'Sensor fiber characterization/5x runs/'
palette = ['#4c3b01','#7c003e','#1b00cd','#008383', '#c902e5', '#ff5e45']

files = ['oldthread_30percent_5x_synced.csv',
         'oldthread_sensorfiber_5x_1_synced.csv',
         'oldthread_sensorfiber_5x_3_synced.csv',
         'oldthread_sensorfiber_5x_4_synced.csv',
         'oldthread_sensorfiber_5x_5_synced.csv',
         'oldthread_sensorfiber_5x_6_synced.csv'
         ]
for i,file in enumerate(files):
    df = pd.read_csv(os.path.join(dataPath,file), header=None)
    df['res_change'] = (df[3] - df[3][0])*(df[3][0]**-1) *100 #(Ri − R0) · (R0)^−1
    df[1] = 30*df[1]/df[1].max() #scale to 30
    #name = f'Sensor Fiber # {i}' if i!=0 else 'Conductive Thread'
    name = 'Sensor Fiber # 3'
    #valleys /\,/\,/\,/\,/\
    valley_indexes = df.index[(df[1].shift(1)>= df[1]) & (df[1]< df[1].shift(-1))].to_list()
    df["cycle"] = 0
    for x in range(len(valley_indexes)):
        df.loc[valley_indexes[x]:, "cycle"] = x+1

    last_cycle = df.loc[df['cycle']==4].copy()
    last_cycle['cycle_change'] = (last_cycle['res_change'] - last_cycle['res_change'].iloc[0])

    plt.plot(last_cycle[1],last_cycle['cycle_change'], color=palette[i], label=name)

# Plot design
plt.annotate("", xytext=(0, .5), xy=(3, 1.7), arrowprops=dict(arrowstyle="->"))
plt.title('Percent Change in Resistance', fontsize=20)
plt.legend(loc='upper left', fontsize=9)
plt.xlabel('Strain (%)', fontsize=15)
plt.ylabel(u'Δ Resistance (%)', fontsize=15)
plt.grid()
plt.show()