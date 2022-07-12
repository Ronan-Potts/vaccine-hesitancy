"""
This file contains functions which will be used throughout the data cleaning and analysis process. These functions include:

check_float(string): input any string into the function. The output is
    True: if the string is formatted as a float,
    False: otherwise.

column_average(file, column_index): outputs the average of the values in a column of a csv file. Input a csv file (file) and
the index of the column (column_index) which is being averaged.

check_row_index(file, state): outputs the index of the data pertaining to the label "state" in a csv file. Input a csv file
(file) and the row label (state) whose index is being output.

position_isfloat(file, column_index, row_index): checks if a cell in a csv file (file) at a row given by (row_index) and column
given by (column_index) is formatted as a float.
    True: if the string is formatted as a float,
    False: otherwise.

check_necessary_states(file): checks that a file contains the necessary states. Output is a string stating whether any states
are missing and which states, if any, are missing.

get_column(file, column_index): gets all data from a column in a csv file, excluding the header entry.
"""



# checks if a string is formatted as a float
def check_float(string):
    try:
        float(string)
        return True
    except:
        return False

# takes average value of a column in csv file. This function ignores non-float (i.e. NULL or N/A) entries.
def column_average(file, column_index):
    first_line = True
    column_values = []
    for line in open(file):
        if first_line:
            first_line = False
        else:
            line_fields = line.strip('\n').rstrip(',').split(',')
            column_values.append(line_fields[column_index])
    summ = 0
    num = 0
    for item in column_values:
        #ignore non-float entries.
        if check_float(item):
            summ += float(item)
            num += 1
    return summ/num

# outputs the index of the data pertaining to the label "state" in "file".
def check_row_index(file, state):
    i = -1 #-1 because we need to skip the header row which doesn't count
    for line in open(file):
        line_fields = line.strip('\n').rstrip(',').split(',')
        if state == line_fields[0]:
            return i
        i += 1


# checks that a specific cell in a csv file contains data which is formatted as a float.
def position_isfloat(file, column_index, row_index):
    first_line = True
    column_values = []
    for line in open(file):
        if first_line:
            first_line = False
        else:
            line_fields = line.strip('\n').rstrip(',').split(',')
            column_values.append(line_fields[column_index])
    return check_float(column_values[row_index])
    
# checks that a file contains all necessary states in the USA.
def check_necessary_states(file):
    first_line = 0
    statenames = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
              "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
              "IL": "Illinois",
              "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine",
              "MD": "Maryland", "MA": "Massachusetts",
              "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", "MT": "Montana",
              "NE": "Nebraska", "NV": "Nevada",
              "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
              "ND": "North Dakota",
              "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island",
              "SC": "South Carolina", "SD": "South Dakota",
              "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
              "WV": "West Virginia", "WI": "Wisconsin",
              "WY": "Wyoming"}
    invalid_states = []
    file_states = []
    states_file_misses = []
    for line in open(file):
        if first_line in [0,1]:
            first_line += 1
        else:
            line_fields = line.strip('\n').rstrip(',').split(',')
            file_states.append(line_fields[0])
            if line_fields[0] not in (list(statenames.values())):
                invalid_states.append(line_fields[0])

    for state in list(statenames.values()):
        if state not in file_states:
            states_file_misses.append(state)
    
    if len(invalid_states) > 0:
        print("These states are unnecessary:")
        for item in invalid_states:
            print(item)
    else:
        print("All states are necessary.")
    if len(states_file_misses) > 0:
        print("You are missing these states:")
        for item in states_file_misses:
            print(item)
    else:
        print("You are not missing any states.")


# gets all data in a given column excluding the header entry
def get_column(file, column_index):
    first_line = True
    vec = []
    for line in open(file):
        if first_line:
            first_line = False
        else:
            line_fields = line.strip('\n').rstrip(',').split(',')
            if check_float(line_fields[column_index]):
                vec.append(float(line_fields[column_index]))
            else:
                vec.append(line_fields[column_index])
    return vec
