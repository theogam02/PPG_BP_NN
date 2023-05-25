import csv
from collections import defaultdict

def calculate_group_averages(input_file, output_file):
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

# Example usage
calculate_group_averages('wave3 - Copy (3).csv', 'avtest.csv')
