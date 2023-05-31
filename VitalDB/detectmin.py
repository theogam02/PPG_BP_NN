import csv

def find_minima(filename, threshold):
    minima_indices = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        data = list(reader)

    amplitude_column = [float(row[2]) for row in data]

    below_threshold = False
    current_min = float('inf')
    current_min_index = -1

    for index, amplitude in enumerate(amplitude_column):
        if amplitude < threshold:
            below_threshold = True
            if amplitude < current_min:
                current_min = amplitude
                current_min_index = int(data[index][0])  # Index value from the first column
        elif below_threshold:
            minima_indices.append(current_min_index)
            current_min = float('inf')
            current_min_index = -1
            below_threshold = False

    return minima_indices

# Example usage
filename = 'wave3.csv'
threshold = 30
minima_indices = find_minima(filename, threshold)
print("Minima indices:", minima_indices)
