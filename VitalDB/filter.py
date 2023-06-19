import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sci
from scipy.signal import butter, filtfilt
from scipy.interpolate import splrep, splev
from scipy.interpolate import interp1d
from scipy.signal import argrelextrema

######################################################################

def read_csv(file_path, column):
    file = pd.read_csv(file_path)
    return file

######################################################################x

def signal_plot(file):
    file.plot(title='PPG', x='Time', y='SNUADC/PLETH')
    plt.show()

######################################################################

def get_time(file):
    col = np.array(file['Time'])
    return col

######################################################################

def get_ppg(file):
    col = np.array(file['SNUADC/PLETH'])
    return col

######################################################################

def filter_ppg(ppg, time):

    cutoff_freq_2 = 25
    order = 4  

    nyquist_freq = 0.5 / 0.002

    normalized_cutoff_freq_2 = cutoff_freq_2 / nyquist_freq

    b, a = butter(order, normalized_cutoff_freq_2, btype='low', analog=False, output='ba')
    ppg_filtered = filtfilt(b, a, ppg)



    # Plot the original and filtered signals
    # plt.figure(figsize=(6, 6))
    # plt.plot(time, ppg, label='Original PPG signal')
    # plt.plot(time, ppg_filtered, label='Filtered PPG signal')
    # plt.xlabel('Time')
    # plt.ylabel('Amplitude')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    return ppg_filtered

######################################################################

def time_domain_features(time,ppg,fall_ppg, max_ppg, prev_min_ppg, max_time, prev_min_ppg_time):
    
    rise = max_ppg - prev_min_ppg
    fall = max_ppg - fall_ppg

    percantages = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

    rise_levels = prev_min_ppg + np.multiply(percantages,rise)
    fall_levels = max_ppg - np.multiply(percantages,fall)
    for level in fall_levels:
        level = 1-level
        level += 0.1

    rise_levels = rise_levels[:-1]
    # print('Prev_Min_PPG:'+ str(prev_min_ppg))
    # print('Max_PPG:'+ str(max_ppg))
    # print('Rise steps:'+ str(rise_levels[0]-prev_min_ppg))

    # print('Rise:'+ str(rise))
    # print('Rise Levels:'+ str(rise_levels))
    # print('Fall:'+ str(fall))
    # print('Fall Levels:'+ str(fall_levels))

    rise_level_times = []
    fall_level_times = []


    for level in rise_levels:
        for i in range(len(ppg)):
            if(ppg[i] >= level):
                rise_level_times.append(time[i])
                break

    for level in fall_levels:
        for i in range(len(ppg)):
            # if i == len(ppg) - 1: print(ppg[i])
            if(i >= np.where(time == max_time)[0]):
                if(ppg[i] - 0.00001 <= level):
                    fall_level_times.append(time[i])
                    break
            
    # print('Rise Levels:'+ str(rise_levels))
    # print('Rise Level Times:'+ str(rise_level_times))

    # print('Fall Levels:'+ str(fall_levels))
    # print('Fall Level Times:'+ str(fall_level_times))

    

    rise_levels = np.concatenate(([prev_min_ppg], rise_levels))
    rise_level_times = np.concatenate(([prev_min_ppg_time], rise_level_times))
    fall_levels = np.concatenate(([max_ppg], fall_levels))
    fall_level_times = np.concatenate(([max_time], fall_level_times))
    # print('rise_levels:', len(rise_levels), 'rise_level_times:', len(rise_level_times))
    # print('fall_levels:', len(fall_levels), 'fall_level_times:', len(fall_level_times))
    # for i in range(len(fall_levels)):
    #     print('Fall level number ' + str(i) + ' is : ' + str(fall_levels[i]))
    # for i in range(len(fall_level_times)):
    #     print('Fall level number ' + str(i) + ' is : ' + str(fall_level_times[i]))


    fall_times_reversed = fall_level_times[::-1]    



    selected_levels = fall_levels
    selected_levels = np.concatenate((rise_levels, selected_levels))
    selected_times = fall_level_times
    selected_times = np.concatenate((rise_level_times, selected_times))

    # print('Length of fall_levels:' + str(len(fall_levels)))
    # print('Length of rise_levels:' + str(len(rise_levels)))
    # print('Length of fall_level_times:' + str(len(fall_level_times)))
    # print('Length of rise_level_times:' + str(len(rise_level_times)))
    # print('Length of selected_levels:' + str(len(selected_levels)))
    # print('Length of selected_times:' + str(len(selected_times)))

    # print('Rise level times ' + str(rise_level_times))
    # print('Fall level times ' + str(fall_level_times))

    # plt.plot(selected_times, selected_levels, marker='o')
    # plt.plot(time,ppg)
    # plt.xlabel('Time')
    # plt.ylabel('Levels')
    # plt.title('Selected Levels Over Time')
    # #plt.legend()
    # plt.grid(True)
    # plt.show()

    rise_time_differences_from_max_time = []
    for time in rise_level_times:
        if(time != max_time):
            rise_time_differences_from_max_time.append(max_time-time)

    rise_time_differences_from_max_time_reversed = rise_time_differences_from_max_time[::-1]
    
    # print('Rise time differences from max time: ' + str(rise_time_differences_from_max_time))
    # print('Reversed Rise time differences from max time: ' + str(rise_time_differences_from_max_time_reversed))
    
    fall_time_differences_from_max_time = []
    for time in fall_level_times:
        if(time != max_time):
            fall_time_differences_from_max_time.append(time-max_time)
    
    #print('Fall time differences from max time: ' + str(fall_time_differences_from_max_time))

    time_differences_from_max_time = []
    for time in selected_times:
        if(time != max_time):
            time_differences_from_max_time.append(np.abs(max_time-time))
    
    #print('Time differences from max time : ' + str(time_differences_from_max_time))


    level_time_ratios = np.abs(np.divide(fall_time_differences_from_max_time , rise_time_differences_from_max_time_reversed))
    level_differences = np.abs(np.subtract(fall_time_differences_from_max_time , rise_time_differences_from_max_time_reversed))

    # level_time_ratios = level_time_ratios[::-1]
    # level_differences = level_differences[::-1]
   
    # print('Level differences:', str(level_differences))
    # print('Level time ratios:', str(level_time_ratios))
    
   

    time_features = np.append(np.append(time_differences_from_max_time , level_differences) , level_time_ratios) 

    return time_features

######################################################################

def time_derivative_features(time, ppg):
    
    ppg_first_derivative = np.gradient(ppg)
    ppg_second_derivative = np.gradient(ppg_first_derivative)


    ppg_local_min_times = time[argrelextrema(ppg, np.less)[0]]
    ppg_local_min_values = ppg[argrelextrema(ppg, np.less)[0]]

    ppg_local_min_values = np.insert(ppg_local_min_values, 0, ppg[0])
    ppg_local_min_times = np.insert(ppg_local_min_times, 0, time[0])

    if(ppg_local_min_values[-1] != ppg[-1]):

        ppg_local_min_values = np.insert(ppg_local_min_values, -1, ppg[-1])
        ppg_local_min_times = np.insert(ppg_local_min_times, -1, time[-1])

    ppg_local_max_times = time[argrelextrema(ppg, np.greater)[0]]
    ppg_local_max_values = ppg[argrelextrema(ppg, np.greater)[0]]

    # if(len(ppg_local_min_times) >= 2):
    #     ppg_local_min_times = ppg_local_min_times[:2]
    #     ppg_local_min_values = ppg_local_min_values[:2]
    # else:
    #     ppg_local_min_times = ppg_local_min_times[0]
    #     ppg_local_min_values = ppg_local_min_values[0]

    
    
    deriv_local_min_times = time[argrelextrema(ppg_first_derivative, np.less)[0]]
    deriv_local_min_values = ppg_first_derivative[argrelextrema(ppg_first_derivative, np.less)[0]]

    deriv_local_max_times = time[argrelextrema(ppg_first_derivative, np.greater)[0]]
    deriv_local_max_values = ppg_first_derivative[argrelextrema(ppg_first_derivative, np.greater)[0]]



    second_deriv_local_min_times = time [argrelextrema(ppg_second_derivative, np.less)[0]]
    second_deriv_local_min_values = ppg_second_derivative[argrelextrema(ppg_second_derivative, np.less)[0]]

    second_deriv_local_max_times = time[argrelextrema(ppg_second_derivative, np.greater)[0]]
    second_deriv_local_max_values = ppg_second_derivative[argrelextrema(ppg_second_derivative, np.greater)[0]]



    # plt.figure(figsize=(6, 6))
    # plt.subplot(3, 1, 1)
    # plt.plot(time, ppg)
    # plt.scatter(ppg_local_min_times, ppg_local_min_values, color='r', label='Local Minima')
    # plt.scatter(ppg_local_max_times, ppg_local_max_values, color='g', label='Local Maxima')
    # plt.title('PPG Signal')
    # plt.xlabel('Time')
    # plt.ylabel('Amplitude')

    # plt.subplot(3, 1, 2)
    # plt.plot(time, ppg_first_derivative)
    # plt.scatter(deriv_local_min_times, deriv_local_min_values, color='r', label='Local Minima')
    # plt.scatter(deriv_local_max_times, deriv_local_max_values, color='g', label='Local Maxima')
    # plt.title('Differentiated PPG Signal')
    # plt.xlabel('Time')
    # plt.ylabel('Rate of Change')

    # plt.subplot(3, 1, 3)
    # plt.plot(time, ppg_second_derivative)
    # plt.scatter(second_deriv_local_min_times, second_deriv_local_min_values, color='r', label='Local Minima')
    # plt.scatter(second_deriv_local_max_times, second_deriv_local_max_values, color='g', label='Local Maxima')
    # plt.title('Second Derivative of PPG Signal')
    # plt.xlabel('Time')
    # plt.ylabel('Second Derivative')


    # plt.tight_layout()
    # plt.show()

    time_deriv_features = np.append(np.append(np.append(np.append(np.append(np.append(np.append(np.append(np.append(np.append(np.append(ppg_local_min_values[0:2] , ppg_local_min_times[0:2]) , ppg_local_max_values[0]) , ppg_local_max_times[0]) , deriv_local_min_values[0:1]) , deriv_local_min_times[0:1]) , deriv_local_max_values[0:1]) , deriv_local_max_times[0:1]) , second_deriv_local_min_values[0:2]) , second_deriv_local_min_times[0:2]) ,second_deriv_local_max_values[0:2]) , second_deriv_local_max_times[0:2])

    return time_deriv_features
    
######################################################################

def frequency_domain_features(ppg):
        
    ppg_fourier = np.fft.fft(ppg)

    sampling_freq = 1/0.002

    # frequencies = np.fft.fftfreq(len(ppg), 1/sampling_freq)
    frequencies = np.fft.fftfreq(len(ppg), d=1/sampling_freq)


    positive_indices = np.where(frequencies >= 0)
    positive_fourier_values = ppg_fourier[positive_indices]
    positive_fourier_frequencies = frequencies[positive_indices]

    # print(str(np.abs(positive_fourier_values)))
    # print(str(positive_fourier_frequencies))


    fourier_local_min_frequencies = positive_fourier_frequencies[argrelextrema(np.abs(positive_fourier_values), np.less)[0]]
    fourier_local_min_values = np.abs(positive_fourier_values)[argrelextrema(np.abs(positive_fourier_values), np.less)[0]]

    fourier_local_max_frequencies = positive_fourier_frequencies[argrelextrema(np.abs(positive_fourier_values), np.greater)[0]]
    fourier_local_max_values = np.abs(positive_fourier_values)[argrelextrema(np.abs(positive_fourier_values), np.greater)[0]]

    fourier_first_local_max_frequencies = fourier_local_max_frequencies[0:1] 
    fourier_first_local_max_values = fourier_local_max_values[0:1]
    fourier_first_local_min_frequencies = fourier_local_min_frequencies[0:1]   
    fourier_first_local_min_values = fourier_local_min_values[0:1]


    first_local_min_index = 0
    second_local_min_index = 0
    
    first_index_found = False

    for i in range(len(positive_fourier_frequencies)):
        for j in range(len(fourier_local_min_frequencies)):
            if positive_fourier_frequencies[i] == fourier_local_min_frequencies[j]:
                first_local_min_index = i
                first_index_found = True
                break
        if first_index_found == True:
            break
    second_index_found = False

    for i in range(len(positive_fourier_frequencies)):
        for j in range(len(fourier_local_min_frequencies)):
            if positive_fourier_frequencies[i] == fourier_local_min_frequencies[j] and i != first_local_min_index:
                second_local_min_index = i
                second_index_found = True
                break
        if second_index_found == True:
            break



    # plt.figure(figsize=(8, 6))
    # plt.plot(positive_fourier_frequencies, np.abs(positive_fourier_values), label='PPG signal')
    # plt.scatter(fourier_local_min_frequencies, fourier_local_min_values, color='g', label='Local Minima')
    # plt.scatter(fourier_local_max_frequencies, fourier_local_max_values, color='r', label='Local Maxima')
    # plt.xlabel('Time')
    # plt.ylabel('Amplitude')
    # plt.xlim(0,20)
    # plt.legend()
    # plt.grid(True)
    # plt.show()

   



    freq_resolution = sampling_freq / len(positive_fourier_frequencies)

    full_power = np.trapz(np.abs(positive_fourier_values) , positive_fourier_frequencies) * freq_resolution

    first_peak_power = np.trapz(np.abs(positive_fourier_values[0 : first_local_min_index + 1]), positive_fourier_frequencies[0:first_local_min_index + 1]) * freq_resolution

    second_peak_power = np.trapz(np.abs(positive_fourier_values[first_local_min_index : second_local_min_index + 1]),positive_fourier_frequencies[first_local_min_index : second_local_min_index + 1]) * freq_resolution

    average_power = full_power / len(positive_fourier_frequencies)

    # print('Area below the FOurier Transform: ' + str(full_power))
    # print('Area below the first Peak: ' + str(first_peak_power))
    # print('Area below the second Peak: ' + str(second_peak_power))

    # print('First local minimum index: ' + str(first_local_min_index) + ' Frequency: ' + str(fourier_local_min_frequencies[0]))
    # print('Second local minimum index: ' + str(second_local_min_index) + ' Frequency: ' + str(fourier_local_min_frequencies[1]))

    # print('The length of the positive fourier frequencies is ' + str(len(positive_fourier_frequencies)))
    # print('The length of the entire fourier frequencies is ' + str(len(frequencies)))

    # print('The average power  is ' + str(average_power))


    relative_powers = []
    
    relative_powers.append(np.trapz(np.abs(positive_fourier_values[0 : 2]), positive_fourier_frequencies[0 : 2]) * freq_resolution / full_power)
    relative_powers.append(np.trapz(np.abs(positive_fourier_values[1 : 3]), positive_fourier_frequencies[1 : 3]) * freq_resolution / full_power)
    relative_powers.append(np.trapz(np.abs(positive_fourier_values[2 : 4]), positive_fourier_frequencies[2 : 4]) * freq_resolution / full_power)
    relative_powers.append(np.trapz(np.abs(positive_fourier_values[3 : 5]), positive_fourier_frequencies[3 : 5]) * freq_resolution / full_power)
    relative_powers.append(np.trapz(np.abs(positive_fourier_values[4 : 6]), positive_fourier_frequencies[4 : 6]) * freq_resolution / full_power)
    relative_powers.append(np.trapz(np.abs(positive_fourier_values[5 : 7]), positive_fourier_frequencies[5 : 7]) * freq_resolution / full_power)

    # print(relative_powers)

    # print('The relative power from 0 - 1 Hz is ' + str(relative_powers[0]))
    # print('The relative power from 1 - 2 Hz is ' + str(relative_powers[1]))
    # print('The relative power from 2 - 3 Hz is ' + str(relative_powers[2]))
    # print('The relative power from 3 - 4 Hz is ' + str(relative_powers[3]))
    # print('The relative power from 4 - 5 Hz is ' + str(relative_powers[4]))
    # print('The relative power from 5 - 6 Hz is ' + str(relative_powers[5]))

    vals = [fourier_first_local_min_values , fourier_first_local_min_frequencies , fourier_first_local_max_values , fourier_first_local_max_frequencies , full_power, first_peak_power , second_peak_power , average_power , relative_powers]
    # frequency_features = np.append(np.append(np.append(np.append(np.append(np.append(np.append(np.append(fourier_first_local_min_values , fourier_first_local_min_frequencies) , fourier_first_local_max_values) , fourier_first_local_max_frequencies) , full_power) , first_peak_power) , second_peak_power) , average_power) , relative_powers)
    frequency_features = np.append(np.append(np.append(np.append(np.append(np.append(np.append(np.append(fourier_first_local_min_values , fourier_first_local_min_frequencies) , fourier_first_local_max_values) , fourier_first_local_max_frequencies) , full_power) , first_peak_power) , second_peak_power), average_power) , relative_powers)

    return frequency_features

######################################################################
######################################################################
######################################################################
######################################################################
######################################################################
######################################################################

# ---------------- Main: ------------------------------------------------------------------------------------
def features(fileName):
    file_path = fileName

    file = read_csv(file_path, 'Time')

    time = get_time(file)
    ppg = get_ppg(file)

    #print('Length of ppg:'+ str(len(ppg)))


    all_features = []


    ppg_raw = ppg.copy()
    ppg = filter_ppg(ppg, time)
    lowest_ppg = min(ppg)
    ppg = ppg - lowest_ppg




    ppg_local_min_times = time[argrelextrema(ppg, np.less)[0]]
    ppg_local_min_values = ppg[argrelextrema(ppg, np.less)[0]]
    ppg_local_max_times = time[argrelextrema(ppg, np.greater)[0]]
    ppg_local_max_values = ppg[argrelextrema(ppg, np.greater)[0]]

    ppg_local_min_values = np.insert(ppg_local_min_values, 0, ppg[0])
    ppg_local_min_times = np.insert(ppg_local_min_times, 0, time[0])

    if(ppg_local_min_values[-1] != ppg[-1]):

        ppg_local_min_values = np.insert(ppg_local_min_values, -1, ppg[-1])
        ppg_local_min_times = np.insert(ppg_local_min_times, -1, time[-1])

    prev_min_ppg = ppg[0]
    prev_min_ppg_time = time[0]

    max_ppg = max(ppg)
    max_ppg_index = np.where(ppg == max_ppg)[0]
    max_time = time[max_ppg_index][0]


    # min_ppg = min(ppg)s
    # min_ppg_index = np.where(ppg == min_ppg)[0]
    # min_time = time[min_ppg_index][0]

    min_ppg = ppg_local_min_values[-1]
    min_time = ppg_local_min_times[-1]


    # if(len(ppg_local_min_values)>2):
    #     fall_ppg = ppg_local_min_values[-1]
    #     fall_ppg_time = ppg_local_min_times[1]
    # else:
    #     fall_ppg = min_ppg
    #     fall_ppg_time = min_time

    fall_ppg = ppg[-1]


    # print('Min_ppg_value: ' + str(min_ppg))
    # print('Min_ppg_time: ' + str(min_time))



    # prev_max_time = 100.746
    # prev_min_time = 101.492

    #max_time_difference = max_time - prev_max_time         ####probs not needed here
    min_time_difference = min_time - prev_min_ppg_time


    pulse_period = 72
    #print('Pulse Period:'+ str(pulse_period))

    heart_rate = 60/pulse_period
    #print('Heart Rate:'+ str(heart_rate))



    derivative_features = time_derivative_features(time,ppg)



    time_features = time_domain_features(time,ppg,fall_ppg, max_ppg, prev_min_ppg, max_time, prev_min_ppg_time)



    frequency_features = frequency_domain_features(ppg)


    features = np.append(np.append(time_features,derivative_features),frequency_features)
    # print('\nThere are ' + str(len(features)) + ' features extracted.\n')

    # for i in range(len(features)):
    #     print('Feature number ' + str(i+1) + ' is : ' + str(features[i]))
    return features


    