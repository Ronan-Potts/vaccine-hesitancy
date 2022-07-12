import statistics
import linecache
import sys, os
sys.path.append(os.path.join('../', os.path.dirname(sys.path[0])))
from data_functions import *

#get header row
header = linecache.getline("group_data/my_working_data.csv", 1).rstrip('\n').split(',')

#column averages and deviations will be used to calculate z-scores
column_averages = []
for i in range(1, 18):
    column_averages.append(column_average("group_data/my_working_data.csv", i))
column_deviations = []
for i in range(1, 18):
    column = get_column("group_data/my_working_data.csv", i)
    deviation = statistics.stdev(column)
    column_deviations.append(deviation)

f1 = open("aggregations/largest_z-score.txt", "w")
f1.write('State' + " & " + 'z-score' + " & " + 'True value' + " & " + 'Category' + ' \\'+ '\\' + '\n')
f1.write('\hline' + '\n')
first_line = 0
for line in open("group_data/my_working_data.csv"):
    if first_line <= 1:
        first_line += 1
    else:
        line_fields = line.strip('\n').rstrip(',').split(',')
        #duplicate line fields to have one copy of z-score data and one copy of data in normal units
        old_line = line_fields.copy()
        i = 1
        while i < len(line_fields)-1:
            #find z-score of all data in line_fields
            line_fields[i] = (float(line_fields[i])-column_averages[i-1])/column_deviations[i-1]
            i += 1
        #below I calculate the total aggregate (largest z-score overall) and find other data associated
        #with it such as state and what the data refers to.
        if first_line == 2:
            first_line += 1
            total_aggregate = max(line_fields[1:-1])
            total_state = line_fields[0]
            field = header[line_fields.index(max(line_fields[1:-1]))]
            real_value = float(old_line[line_fields.index(max(line_fields[1:-1]))])
        if max(line_fields[1:-1]) > total_aggregate:
            total_aggregate = max(line_fields[1:-1])
            total_state = line_fields[0]
            field = header[line_fields.index(max(line_fields[1:-1]))]
            real_value = float(old_line[line_fields.index(max(line_fields[1:-1]))])
            
        f1.write(line_fields[0] + " & " + str(round(max(line_fields[1:-1]), 2)) + " & " + str(round(float(old_line[line_fields.index(max(line_fields[1:-1]))]), 2)) + " & " + '(' + header[line_fields.index(max(line_fields[1:-1]))] + ')' + ' \\'+ '\\' + '\n')
        f1.write('\hline' + '\n')
f1.write("Largest z-score" + ' & ' + str(round(total_aggregate, 2)) + ' & ' + str(round(real_value, 2)) + ' & ' + '(' + total_state + ' - ' + field + ')' + ' \\\ ' + '\n')
f1.write('\\hline')
f1.close()

print('\n'*5)

#note that we bin the math_composite_avg scores since these had no missing values in the original dataset
#the get_column() function was written in the data_functions.py file
math_composite_avg = sorted(get_column("group_data/my_working_data.csv", 5))
len_math_comp = len(math_composite_avg)
bins = {1:-1, 2:-1, 3:-1, 4:-1, 5:-1, 6:-1, 7:-1, 8:-1, 9:-1, 10:-1} #for deciles a value of -1 is given to prevent intereference with max() function
i = 0
while i < len_math_comp:
    bin_num = int((((i/len_math_comp)*10) + 1)//1) #there are 5 values per bin
    bins[bin_num] = max(math_composite_avg[i], bins[bin_num])
    i += 1

#redefine math_composite_avg so that its values align with the states in the states list
math_composite_avg = get_column("group_data/my_working_data.csv", 5)
states = get_column("group_data/my_working_data.csv", 0)

#below I add the states to each score
for key in bins:
    value = bins[key]
    i = 0
    while i < len(math_composite_avg):
        if math_composite_avg[i] == value:
            bins[key] = [bins[key], states[i]]
        i += 1

#write information in a text file that can be copy/pasted into a LaTeX table environment
f2 = open("aggregations/binned_math_comp.txt", "w")
f2.write('Decile' + " & " + 'Score' + " & " + 'State' + ' \\'+ '\\' + '\n')
f2.write('\hline' + '\n')
for key in bins:
    f2.write(str(key) + " & " + str(round(bins[key][0], 2)) + " & " + bins[key][1] + ' \\'+ '\\' + '\n')
    f2.write('\hline' + '\n')
f2.close()





#the get_column() function is defined in the data_functions.py file
votes = get_column("group_data/my_working_data.csv", -2)
votes = [int(x//0.1) for x in votes]
states = get_column("group_data/my_working_data.csv", 0)
vac = get_column("group_data/my_working_data.csv", 14)
degree_proportion = get_column("group_data/my_working_data.csv", 13)
region = get_column("group_data/my_working_data.csv", 18)

#place all information above into a single list
i = 0
while i < len(votes):
    votes[i] = [states[i], votes[i], vac[i], degree_proportion[i], region[i]]
    i += 1

#sort the list based on the bin value
votes = sorted(votes, key = lambda x: x[1])

#write information in a text file that can be copy/pasted into a LaTeX table environment
f3 = open("aggregations/democrat_vaccine_bins.txt", "w")
f3.write('Location' + " & " + 'Voting Decile' + " & " + 'Vaccinated Proportion' + ' & ' + "Proportion with Bachelor's degree" + ' & ' + 'Region' + ' \\'+ '\\' + '\n')
f3.write('\hline' + '\n')
for item in votes:
    f3.write(item[0] + " & " + str(item[1]) + " & " + str(round(item[2], 2)) + ' & ' + str(round(item[3], 2)) + ' & ' + item[4] + ' \\'+ '\\' + '\n')
    f3.write('\hline' + '\n')
f3.close()



#define bins for variables
binned_votes = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
bin_nums = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}

#write information in a text file that can be copy/pasted into a LaTeX table environment
f4 = open("aggregations/democrat_bins_averages.txt", "w")
f4.write('Voting Decile' + " & " + 'Vaccinated Proportion' + ' & ' + "Proportion with Bachelor's degree" + ' \\'+ '\\' + '\n')
f4.write('\hline' + '\n')
for item in votes:
    #write information from votes string into the binned_votes dictionary
    if len(binned_votes[item[1]]) == 0:
        binned_votes[item[1]] = item[2:-1]
        bin_nums[item[1]] = 1 #this counter is initialised to perform an average
    else:
        binned_votes[item[1]][0] += item[2:-1][0]
        binned_votes[item[1]][1] += item[2:-1][1]
        bin_nums[item[1]] += 1
for key in binned_votes:
    if len(binned_votes[key]) > 0:
        #calculate the average for each bin
        binned_votes[key] = [round(binned_votes[key][0]/bin_nums[key], 2), round(binned_votes[key][1]/bin_nums[key], 2)]
        #finish writing the information into a text file to be copy/pasted into a LaTeX table environment
        f4.write(str(key) + ' & ' + str(binned_votes[key][0]) + ' & ' + str(binned_votes[key][1]) + ' \\'+ '\\' + '\n')
        f4.write('\hline' + '\n')
f4.close()


