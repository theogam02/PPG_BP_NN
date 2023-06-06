import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sci
from scipy.signal import butter, filtfilt
from scipy.interpolate import splrep, splev
from scipy.interpolate import interp1d
from scipy.signal import argrelextrema
from scipy.signal import argrelmin
from collections import defaultdict
######################################################################

def read_csv(file_path, column_name):
    file = pd.read_csv(file_path)
    return file

######################################################################


def get_time(file):
    col = np.array(file[file.columns[0]])
    return col


######################################################################

def get_ppg(file):
    col = np.array(file['SNUADC/PLETH'])
    return col

######################################################################
def filter_ppg(ppg_raw, time):

    cutoff_freq_1 = 0.1 
    cutoff_freq_2 = 15
    order = 4  

    nyquist_freq = 0.5 / 0.002

    normalized_cutoff_freq_1 = cutoff_freq_1 / nyquist_freq
    normalized_cutoff_freq_2 = cutoff_freq_2 / nyquist_freq

    b, a = butter(order, [normalized_cutoff_freq_1 , normalized_cutoff_freq_2], btype='band', analog=False, output='ba')
    ppg_filtered = filtfilt(b, a, ppg_raw)


    return ppg_filtered

######################################################################

def getmin(ppg,time):
    mindexes = time[argrelextrema(ppg, np.less,order=190)[0]]

    minvalues= ppg[argrelextrema(ppg, np.less, order=190)[0]]
    print(mindexes)
    print(minvalues)
    plt.plot(time,ppg_fil)
    plt.plot(mindexes, minvalues, 'o')

    plt.show()
    return mindexes

######################################################################
def countset(csv_file, indexes_of_interest):
    updated_rows = []  # To store the updated rows

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the first row (header)
        updated_rows.append(header)  # Add the header to the updated rows

        for row in reader:
            if int(row[0]) in indexes_of_interest:
                row[0] = '0'  # Change the value to 0
                updated_rows.append(row)
            else:
                updated_rows.append(row)

    # Update subsequent indexes between each index of interest
    count = 1
    for i in range(len(updated_rows)):
        if updated_rows[i][0] == '0':
            count = 1
        else:
            updated_rows[i][0] = str(count)
            count += 1

    # Write the updated rows back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)    

######################################################################

def average(input_file, output_file):
    # Dictionary to store sum and count for each group
    group_totals = defaultdict(lambda: [0, 0])

    with open(input_file, 'r') as file:
        csv_reader = csv.reader(file)

        # Skip the header
        next(csv_reader)

        # Iterate over the rows
        for row in csv_reader:
            group = int(row[0])
            value = float(row[2])

            # Update the sum and count for the group
            group_totals[group][0] += value
            group_totals[group][1] += 1

    with open(output_file, 'w', newline='') as file:
        csv_writer = csv.writer(file)

        # Write the averages to the new CSV file
        for group, (total, count) in group_totals.items():
            average = total / count if count > 0 else 0
            csv_writer.writerow([group, average])
######################################################################
def sort(csv_file):
    # Read the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Sort rows based on the first column
    sorted_rows = sorted(rows, key=lambda x: int(x[0]))

    # Write the sorted rows back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sorted_rows)

    header = ['Time', 'SNUADC/PLETH']

    # Read the existing data from the file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

# Add the header to the data
    data.insert(0, header)

# Write the updated data back to the file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
##############################################################



#Main

#define file path
file_path = 'wave35.csv'

#read csv file
file = read_csv(file_path, 'Time')

time = get_time(file)
ppg = get_ppg(file)

#filter PPG signal
ppg_fil = filter_ppg(ppg, time)

#Find minimums
mindexes = getmin(ppg_fil,time)

#Change indexes based on minimums
countset(file_path , mindexes)

#get average
average(file_path, 'a_output.csv')

#sort columns
sort('a_output.csv')


#plot output
data = pd.read_csv('a_output.csv')

# Extract the values from column 1 (x-axis) and column 3 (y-axis)
x = data.iloc[:, 0]
y = data.iloc[:, 1]

# Plot the data
plt.plot(x, y)

# Set the labels for x-axis and y-axis
plt.xlabel('Index')
plt.ylabel('Signal Value')

plt.title('Averaged Wave')


plt.show()









