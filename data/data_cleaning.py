import linecache
import statistics
import csv
from operator import itemgetter
import sys, os
sys.path.append(os.path.join('../', os.path.dirname(sys.path[0])))
from data_functions import *

# this function checks that there are no states in raw_data.csv which are not needed, and identifies any missing states
check_necessary_states("data/raw_data.csv")

# below I check for negative values, which must be incorrect.
first_line = 0
negative_values = []
header = linecache.getline("data/raw_data.csv", 2).rstrip('\n').split(',')
for line in open("data/raw_data.csv"):
    if first_line in [0,1]:
        first_line += 1
    else:
        line_fields = line.strip('\n').rstrip(',').split(',')
        i = 1
        while i < 13:
            item = line_fields[i]
            if check_float(item) and float(item) < 0:
                negative_values.append([line_fields[0], header[i], item])
            i += 1
if len(negative_values) > 0:
    print("You have " + str(len(negative_values)) + " negative values:")
    for item in negative_values:
        print("  " + str(item))
else:
    print("You have no negative values.")
    
                    

# This is the actual cleaning part. Here I replace all empty values with the average of that column

with open("data/clean_data.csv", 'w') as new_file:
    new_lines = []
    first_line = 0
    for line in open("data/raw_data.csv"):
        if first_line == 0:
            first_line += 1
        elif first_line == 1:
            new_file.write(line)
            first_line += 1
        else:
            line_fields = line.strip('\n').rstrip(',').split(',')
            i = 1
            while i <= 12:
                if not check_float(line_fields[i]):
                    line_fields[i] = str(column_average("data/raw_data.csv", i))
                i += 1
            new_lines.append(line_fields)

    for item in new_lines:
        j = 0
        while j < len(item):
            if j == 0:
                new_file.write(item[j])
            else:
                new_file.write(',')
                new_file.write(item[j])
            j += 1
        new_file.write('\n')
        

# this sorts the rows of clean_data.csv alphabetically, assisting the merging process later on.
first_line = True
with open('data/alphabetical_clean_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    with open('data/clean_data.csv') as file:
        clean = csv.reader(file)
        list = []
        for line in clean:
            if first_line:
                first_line = False
                writer.writerow(line)
            else:
                list.append(line)
    alphabetical = sorted(list, key=itemgetter(0))
    writer.writerows(alphabetical)
    
