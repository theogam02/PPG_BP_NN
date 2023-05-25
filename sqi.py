import pandas as pd
import numpy as np

# Read the CSV file into a pandas DataFrame, skipping the header row
df = pd.read_csv('wave200.csv', skiprows=1, header=None)

# Access the values in the third column, for the average wave files, its column index 1
values = df.iloc[:, 2]

# Calculate the number of samples
num_samples = len(values)

# Calculate the mean and standard deviation of the values
mean_value = np.mean(values)
std_value = np.std(values)

# Calculate the sum of the values
sum_value = 0
for value in values:
   # print(value)
    sum_value += (value- mean_value)**3
    #print(sum_value)

sqi = (1/(num_samples* (std_value**3) )) * sum_value    

# Print the results
print("Number of samples:", num_samples)
print("Mean of values:", mean_value)
print("Standard deviation of values:", std_value)
print("Sqi:", sqi)

