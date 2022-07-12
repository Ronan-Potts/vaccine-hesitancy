import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.cm import ScalarMappable
import sys, os
sys.path.append(os.path.join('../', os.path.dirname(sys.path[0])))


#read file into python and define a few lists
df = pd.read_csv("group_data/my_working_data.csv")

total_vaccinated = (df["Series_Complete_Yes"] / 1000000).to_list()
population = (df["Total Population"] / 1000000).to_list()
p_dem = df["percent_democrat"].to_list()

m, b = np.polyfit(np.array(population), np.array(total_vaccinated), 1)
#define the size of the figure and legend
fig, ax = plt.subplots(figsize=(15, 4))


#grab the 'Blues' colormap from matplotlib.cm
my_cmap = plt.cm.get_cmap('Blues')
#create a list of colours based on percent_democrat
colours = my_cmap(p_dem)
#create the line of best fit

plt.plot(population, m*np.array(population) + b, color='#dbdbdc', linewidth=0.5)
#create the bar plot
points = ax.scatter(population, total_vaccinated, color=colours, edgecolor='gray')


#define a ScalarMappable for the legend
sm = ScalarMappable(cmap=my_cmap, norm=plt.Normalize(0, 100))
sm.set_array([])

#create the colorbar from the ScalarMappable
cbar = plt.colorbar(sm)
cbar.set_label('Percentage of Votes for Democratic Party (%)', rotation=270, labelpad=25)
#labelpad=25 places the label 25 units to the right of its default point

plt.subplots_adjust(bottom=0.25)
plt.ylabel("Vaccinated Population (millions)")
plt.xlabel("Total Population (millions)")
plt.title("Population of vaccinated individuals vs total population in states across the USA")
plt.savefig("charts/3 variable scatter plot.png")


#-------------------------------------------------------------------------------


#read file into python and define a few lists
df = pd.read_csv("group_data/my_working_data.csv")

vac_prop = (df["Vaccinated_Proportion"] * 100).to_list()
state = df["Location"].to_list()
p_dem = df["percent_democrat"].to_list()

#define the size of the figure and legend
fig, ax = plt.subplots(figsize=(15, 4))


#grab the 'Blues' colormap from matplotlib.cm
my_cmap = plt.cm.get_cmap('Blues')
#create a list of colours based on percent_democrat
colours = my_cmap(p_dem)
#create the bar plot
rects = ax.bar(state, vac_prop, color=colours, edgecolor='black')


#define a ScalarMappable for the legend
sm = ScalarMappable(cmap=my_cmap, norm=plt.Normalize(0, 100))
sm.set_array([])

#create the colorbar from the ScalarMappable
cbar = plt.colorbar(sm)
cbar.set_label('Percentage of Votes for Democratic Party (%)', rotation=270, labelpad=25)
#labelpad=25 places the label 25 units to the right of its default point

plt.subplots_adjust(bottom=0.25)
plt.xticks(rotation=90)
plt.ylabel("Percentage of Population that is completely vaccinated (%)")
plt.xlabel("State")
plt.title("Proportion of vaccinated population in each state in the USA")
plt.savefig("charts/Bar Plot.png")


#-------------------------------------------------------------------------------


#read file into python and define a few lists
df = pd.read_csv("group_data/my_working_data.csv")

vaccinated_proportion = (df["Vaccinated_Proportion"] * 100).to_list()
percent_bach = (df["Bachelor's degree or higher"] * 100).to_list()
p_dem = df["percent_democrat"].to_list()

#the stat_scale score has to range from 10 to 100 for size mapping.
stat_scale_score = df["Average Scale Score math_stat"]
#solving the equation (max-x) / (min-x) = 10 for x gives the factor
#I need to subtract from stat_scale_score to have the minimum be equal
#to maximum/10
scale = (10*min(stat_scale_score)-max(stat_scale_score)) / 9
#I then scale the whole vector to range from 10 to 100
stat_scale_score = 100*(stat_scale_score- scale)/(max(stat_scale_score) - scale)


m, b = np.polyfit(np.array(percent_bach), np.array(vaccinated_proportion), 1)
#define the size of the figure and legend
fig, ax = plt.subplots(figsize=(15, 4))


#grab the 'Blues' colormap from matplotlib.cm
my_cmap = plt.cm.get_cmap('Blues')
#create a list of colours based on percent_democrat
colours = my_cmap(p_dem)

#create the line of best fit
plt.plot(percent_bach, m*np.array(percent_bach) + b, color='#dbdbdc', linewidth=0.5)
#create the scatter plot
points = ax.scatter(percent_bach, vaccinated_proportion, color=colours, edgecolor='gray', s=(stat_scale_score).to_list())


#define a ScalarMappable for the legend
sm = ScalarMappable(cmap=my_cmap, norm=plt.Normalize(0, 100))
sm.set_array([])

#create the colorbar from the ScalarMappable
cbar = plt.colorbar(sm)
cbar.set_label('Percentage of Votes for Democratic Party (%)', rotation=270, labelpad=25)
#labelpad=25 places the label 25 units to the right of its default point

handles = points.legend_elements(prop="sizes", alpha=0.3, num=2)[0]
legend2 = ax.legend(handles, [225,249], loc="lower right", title="Statistics Scale Scores")
one = True
for legend_handle in legend2.legendHandles:
    if one:
        legend_handle._legmarker.set_markersize(3.5)
        one = False
    else:
        legend_handle._legmarker.set_markersize(10)

plt.subplots_adjust(bottom=0.25)
plt.ylabel("Percentage of fully vaccinated individuals (%)")
plt.xlabel("Percentage of people with a bachelor's degree or higher (%)")
plt.title("Percentage of fully vaccinated individuals vs percentage of people with a bachelor's degree or higher")
plt.savefig("charts/4 variable scatter plot.png")
