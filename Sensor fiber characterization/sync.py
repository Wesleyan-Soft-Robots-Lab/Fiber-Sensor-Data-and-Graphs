import csv
from datetime import datetime, timedelta
import math

input_ameteks = [\
                #'sensor fibers\oldthread_sensorfiber_5x_1_2024-12-18_14-50-47.csv',\
                #'sensor fibers\oldthread_sensorfiber_5x_3_2024-12-18_17-09-22.csv',\
                #'sensor fibers\oldthread_sensorfiber_5x_4_2024-12-18_19-25-41.csv',\
                #'sensor fibers\oldthread_sensorfiber_5x_5_2024-12-18_21-10-02.csv',\
                #'sensor fibers\oldthread_sensorfiber_5x_6_2_2024-12-18_23-29-10.csv',\
                #'sensor fibers\oldthread_sensorfiber_500x_2024-12-20_09-31-04.csv',\
                #'sensor fibers\oldthread_sensorfiber_repaired_5x_20percentstrain2024-12-19_14-43-38.csv',\
                #'sensor fibers\oldthread_sensorfiber_repaired_5x_30percent_2024-12-19_15-09-43.csv'
                'conductive thread\oldthread_30percent_5x_ametek_formatted.csv'
                ]
input_dmms = [\
             #'sensor fibers/oldthread_sensorfiber_5x_1-dmm-11.csv',\
             #'sensor fibers\oldthread_sensorfiber_5x_3-dmm-11.csv',\
             #'sensor fibers\oldthread_sensorfiber_5x_4-dmm-11.csv',\
             #'sensor fibers\oldthread_sensorfiber_5x_5-dmm-11.csv',\
             #'sensor fibers\oldthread_sensorfiber_5x_6_2-dmm-11.csv',\
             #'sensor fibers\oldthread_sensorfiber_500x-dmm-11.csv',\
             #'sensor fibers\oldthread_sensorfiber_repaired_5x_20percentstrain-dmm-11.csv',\
             #'sensor fibers\oldthread_sensorfiber_repaired_5x_30percentstrain-dmm-11.csv'
             'conductive thread\oldthread_30percent_5x-dmm-11.csv'
             ]
output_filenames = [\
                    #'sensor fibers\oldthread_sensorfiber_5x_1_synced.csv',\
                    #'sensor fibers\oldthread_sensorfiber_5x_3_synced.csv',\
                    #'sensor fibers\oldthread_sensorfiber_5x_4_synced.csv',\
                    #'sensor fibers\oldthread_sensorfiber_5x_5_synced.csv',\
                    #'sensor fibers\oldthread_sensorfiber_5x_6_synced.csv',\
                    #'sensor fibers\oldthread_sensorfiber_500x_synced.csv',\
                    'sensor fibers\oldthread_sensorfiber_repaired_5x_20percentstrain_synced.csv',\
                    'sensor fibers\oldthread_sensorfiber_repaired_5x_30percentstrain_synced.csv'
                    ]

for (ametek_filename, dmm_filename, output_filename) in zip(input_ameteks, input_dmms, output_filenames):

    print(output_filename)
    
    ohms = []
    time_dmm = []
    Ns = []
    mms = []
    time_from_0_ametek = []
    time_ametek = []

    print("Reading Ametek data ...")

    with open(ametek_filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader)
        row = next(reader)
        t0_ametek = datetime.strptime(row[3], "%H:%M:%S")
        dt = timedelta(days=0, seconds=0, milliseconds=10, microseconds=0)

        for i in range(3):
            next(reader)
        
        for row in reader:
            time_from_0_ametek.append(float(row[0]))
            Ns.append(float(row[1]))
            mms.append(float(row[3]))

    for i in range(len(mms)):
            time_ametek.insert(0, t0_ametek-i*dt)

    time_ametek = time_ametek[0:-1]

    with open(ametek_filename[:-4] + '_formatted.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(time_ametek)):
            writer.writerow([time_ametek[i], mms[i], Ns[i]])

    print("Reading DMM data ...")

    with open(dmm_filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader)
        for row in reader:
            time_dmm.append(datetime.strptime(row[3], "%H:%M:%S.%f"))
            ohms.append(float(row[2]))

    i = 0
    while not(time_ametek[0].hour == time_dmm[i].hour and time_ametek[0].minute == time_dmm[i].minute and time_ametek[0].second == time_dmm[i].second):
        i = i + 1

    time_dmm = time_dmm[i:]
    ohms = ohms[i:]

    i = len(time_dmm)-1
    while not(time_ametek[-1].hour == time_dmm[i].hour and time_ametek[-1].minute == time_dmm[i].minute and time_ametek[-1].second == time_dmm[i].second):
        i = i - 1

    time_dmm = time_dmm[:i]
    ohms = ohms[:i]

    # Get total number of seconds
    difference = time_dmm[-1] - time_dmm[0]
    length_in_seconds = math.ceil(difference.total_seconds())

    i = 0
    j = 0
    synced_mms = []
    synced_Ns = []
    curr_second = time_ametek[0].second

    while(j < length_in_seconds-1):
        summed_mms = 0.0
        summed_Ns = 0.0
        num_samples = 0.0
        while(time_ametek[i].second == curr_second):
            summed_mms = summed_mms + mms[i]
            summed_Ns = summed_Ns + Ns[i]
            num_samples = num_samples + 1
            i = i + 1
        synced_mms.append(summed_mms/num_samples)
        synced_Ns.append(summed_Ns/num_samples)
        j = j + 1
        curr_second = (curr_second + 1) % 60

    i = 0
    j = 0
    synced_ohms = []
    curr_second = time_dmm[0].second

    while(j < length_in_seconds-1):
        summed_ohms = 0.0
        num_samples = 0.0
        while(time_dmm[i].second == curr_second):
            summed_ohms = summed_ohms + ohms[i]
            num_samples = num_samples + 1
            i = i + 1
        synced_ohms.append(summed_ohms/num_samples)
        j = j + 1
        curr_second = (curr_second + 1) % 60

    print("Saving data ...")

    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(length_in_seconds-1):
            writer.writerow([i, synced_mms[i], synced_Ns[i], synced_ohms[i]])
    
    print("")
