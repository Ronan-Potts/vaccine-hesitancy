import linecache
import statistics
from data_functions import *

import csv
from operator import itemgetter



#this function checks that there are no states in my file which I do not need, and identifies any missing states
check_necessary_states("Ronan_CSV_Education_V1.3.csv")

#below I check for negative values, which must be incorrect.
first_line = 0
negative_values = []
header = linecache.getline("Ronan_CSV_Education_V1.3.csv", 2).rstrip('\n').split(',')
for line in open("Ronan_CSV_Education_V1.3.csv"):
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
    
                    

#This is the actual cleaning part. Here I replace all empty values with the average of that column

with open("clean_education_csv.csv", 'w') as new_file:
    new_lines = []
    first_line = 0
    for line in open("Ronan_CSV_Education_V1.3.csv"):
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
                    line_fields[i] = str(column_average("Ronan_CSV_Education_V1.3.csv", i))
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
        

first_line = True
with open('abc_clean_education_csv.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    with open('clean_education_csv.csv') as file:
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








#this function replaces missing graduation rates by scaling the graduation rates in other columns to the average of the missing rate column
##def fix_empty_graduation1(file, column_index, row_index):
##    line = linecache.getline(file, row_index + 2).split(',') #this gets the line that contains the value you want to fix
##    i = 1
##    other_vals = []
##    column_averages = []
##    while i <= 8:
##        if i != column_index:
##            if check_float(line[i]):
##                column_averages.append(column_average(file, i))
##                other_vals.append(float(line[i]))
##        i += 1
##        
##    column_averages_avg = sum(column_averages)/len(column_averages)
##    average_vals = sum(other_vals)/len(other_vals)
##    weighted_avg = average_vals / column_averages_avg
##
##    new_val = weighted_avg*column_average(file, column_index)
##    return new_val
#this method is not the best. We can see this by looking at Conneticut, which has an above average graduation
#rate for doctorates, and a below average rate for all others. The above average doctorate graduation rate brings
#Conneticut's weighted average to 1.14 - i.e. it's estimate is 14% above the average. If we had to estimate Conneticut's
#<2-year graduation rate, we would have estimated 0.799, which is much larger than 0.659


##def fix_empty_graduation2(file, column_index):
##    return column_average(file, column_index)


#the code below shows that the weighted average method performs worse than just replacing values with the average

##first_line = True
##column_values = []
##for line in open("Ronan_CSV_Education_V1.3.csv"):
##    if first_line:
##        first_line = False
##    else:
##        line_fields = line.strip('\n').rstrip(',').split(',')
##        column_values.append(float(line_fields[2]))
##
##i = 0
##deviation_1 = []
##deviation_2 = []
##while i < len(column_values):
##    deviation_1.append(fix_empty_graduation1("Ronan_CSV_Education_V1.3.csv", 2, i)-column_values[i])
##    deviation_2.append(column_average("Ronan_CSV_Education_V1.3.csv", 2)-column_values[i])
##    i += 1
##
##print(statistics.stdev(deviation_1))
##print(statistics.stdev(deviation_2))
    
