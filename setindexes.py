import csv

def update_csv_file(csv_file, indexes_of_interest):
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

# Example usage
csv_file = 'wave3 - Copy (3).csv'  # Replace with the path to your CSV file
indexes_of_interest =  [20367, 20758, 20835, 21748, 22198, 22715, 22726, 22737, 23161, 23164, 23181, 23523, 24026, 24661, 2, 27500, 27941, 29053, 29377, 29964] # Replace with your list of indexes

update_csv_file(csv_file, indexes_of_interest)
