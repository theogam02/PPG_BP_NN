#code splits track files into 20 sec csv files

import pandas as pd

# Define the file path of the CSV file
csv_file = "track1.csv"

# Read the CSV file 
data = pd.read_csv(csv_file)

# Calculate the number of samples in a 20-second interval
interval_samples = int(20 / 0.002)

# Split the data into 20-second intervals
intervals = [data[i:i+interval_samples] for i in range(0, len(data), interval_samples)]

# make new csv files
for i, interval in enumerate(intervals):
    interval_name = f"wave{i+1}.csv"
    interval.to_csv(interval_name, index=False)
    print(f"Interval {i+1}: {interval_name} created.")

    #[20367, 20758, 20835, 21748, 22198, 22715, 22726, 22737, 23161, 23164, 23181, 23523, 24026, 24661, 2, 27500, 27941, 29053, 29377, 29964]