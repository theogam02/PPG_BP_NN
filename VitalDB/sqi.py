import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def sqitest(file_path):
    skewsqi = 0
    k_sqi =0
    # Read the CSV file into a pandas DataFrame, skipping the header row
    df = pd.read_csv(file_path, skiprows=1, header=None)

    # Access the values in the third column, for the average wave files, its column index 1
    values = df.iloc[:, 1]

    # Calculate the number of samples
    num_samples = len(values)

    # Calculate the mean and standard deviation of the values
    mean_value = np.mean(values)
    std_value = np.std(values)

    min_value = np.min(values)
    max_value = np.max(values)


    #Perfusion
    p_sqi = ((max_value - min_value)/mean_value)*100

    #Kurtosis
    k_sum_value = 0
    for value in values:
    # print(value)
        k_sum_value += (value- (mean_value))**4
        #print(sum_value)

    k_sqi = (1/(num_samples* (std_value**4) )) * k_sum_value    



    #Skew
    # Calculate the sum of the values
    sum_value = 0
    for value in values:
    # print(value)
        sum_value += (value- (mean_value))**3
        #print(sum_value)

    skewsqi = (1/(num_samples* (std_value**3) )) * sum_value    

    #Entropy
    e_sum_value = 0
    for value in values:
    # print(value)
        e_sum_value +=( (value*2) * (np.log(value*2)))
        #print(sum_value)
    e_sqi = e_sum_value *-1

    # Print the results
    # print("Number of samples:", num_samples)
    # print("Mean of values:", mean_value)
    # print("Standard deviation of values:", std_value)
    # print("Skewness Sqi:", skewsqi)
    # print("Kurtosis Sqi:",k_sqi)
    # print("Perfusion Sqi:",p_sqi)
    # print("Entropy Sqi:",e_sqi)


    # Load the CSV file using pandas
    data = pd.read_csv(file_path)

    # Extract the values from column 1 (x-axis) and column 3 (y-axis)
    # x = data.iloc[:, 0]
    # y = data.iloc[:, 1]

    # # Plot the data
    # plt.plot(x, y)

    # # Set the labels for x-axis and y-axis
    # plt.xlabel('X-axis')
    # plt.ylabel('Y-axis')

    # # Add a title to the plot
    # plt.title('CSV Data Plot')

    # # Show the plot
    # plt.show()



    #Test if the file passes the thresholds:
    t = 0
    if skewsqi < 0.3501 or skewsqi >1.5:
        t=1
        # print('skew test failed')
    if k_sqi < 1.5 or k_sqi >3.5:
        t=1
        # print('k test failed')
    if mean_value >1 :
        t=1
    if p_sqi < 20 or p_sqi >200 :
        t=1
    # if e_sqi <80 :
    #     t=1
    #     # print('e test failed')

    # if t == 1:
    #     print('sqi test failed')
    # else :
    #     print('passed')
    return t

# sqitest('a_output.csv')
