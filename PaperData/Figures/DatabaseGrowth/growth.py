


import csv

# Define the path to your CSV file
file_path = 'dbsize.csv' # Current Dir

# Initialize an empty list to store the data
data = []

# Open the CSV file and parse it
with open(file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)

    # Loop through each row in the CSV
    for row in csv_reader:
        # Convert 'Reproducible' and 'All Bugs' to integers
        row['Reported'] = int(row['Reported'])
        row['Reproducible'] = int(row['Reproducible'])
        row['All Bugs'] = int(row['All Bugs'])

        # Append the row (as a dictionary) to our data list
        data.append(row)

# Now 'data' contains all the rows of the CSV file as dictionaries
# print(data)
# print(data)

Timeline = []

Timeline    = ["2016","2017","2018","2019","2020","2021","2022","2023"]

ossfuzz     = [0 for x in range(len(Timeline))]
reproducer  = [0 for x in range(len(Timeline))]
reported    = [0 for x in range(len(Timeline))]
line_data = [
    [],[]
]
for x in data:
    # if x["Date"].split("-")[0] not in Timeline:
    #     continue
    year = x["Date"].split("-")[0]
    month = int(x["Date"].split("-")[1])
    # if month <= 6:
    #     flag = 0
    # else:
    #     flag = 1

    idx = Timeline.index(x["Date"].split("-")[0])
    # Timeline.append(x["Date"])

    # idx = data.index(x)
    v1 = x['Reported']
    v2 = x['Reproducible']
    v3 = x['All Bugs']
    reported[idx]= v1
    reproducer[idx]= v2
    ossfuzz[idx]= v3

    line_data[0].append((v1+v2) / (v1+v2+v3) * 100)
    line_data[1].append((v1) / (v1+v2+v3)* 100)
# import matplotlib.pyplot as plt
# import numpy as np

# color_map = ["#9b59b6", "#e74c3c", "#2ecc71"]

# population_by_continent = {
#     'Fix Located Bugs on ARVO': reported,
#     'Reproducible Bugs on ARVO': reproducer,
#     'Security Bugs on OSS-Fuzz': ossfuzz,
# }
# fig, ax = plt.subplots()
# ax.stackplot(Timeline, population_by_continent.values(),
#              labels=population_by_continent.keys(), alpha=0.8,colors = color_map)
# ax.legend(loc='upper left', reverse=True)
# ax.set_title('Cumulative Reproducible Cases')
# ax.set_xlabel('Time Spent (Month)')
# ax.set_ylabel('Number of people (millions)')

# plt.show()
import matplotlib.pyplot as plt
import numpy as np

# purple, red, green
color_map = ["#9b59b6", "#e74c3c", "#2ecc71"]

population_by_continent = {
    'Fix Located': reported,
    'Reproducible': reproducer,
    'All Vulnerabilities': ossfuzz,
}

# Data for the line graph (example)
  # Replace with your actual data
line_labels = ['Reproduced', 'Fix Located',]
line_colors = {'Reproduced': '#e74c3c', 'Fix Located': '#9b59b6',}
# Create a figure with two subplots (axes)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))  # Adjust figure size as needed

# First plot (Stackplot)
print(Timeline)
ax1.stackplot(Timeline, population_by_continent.values(),
              labels=population_by_continent.keys(), alpha=0.8, colors=color_map)
ax1.legend(loc='upper left', reverse=True,fontsize=20)
ax1.set_title('Vulnerabilities Over Time',fontsize=20)
ax1.set_xlabel('Timestamp',fontsize=20)
ax1.set_ylabel('# Vulnerabilities', fontsize=20)
ax1.set_xticks([x for x in range(len(Timeline))])
ax1.set_xticklabels(Timeline, rotation=45, fontsize=20)
ax1.tick_params(axis='both', labelsize=20)

# Second plot (Line graph)
for data, label in zip(line_data, line_labels):
    ax2.plot([x for x in range(88)], data, label=label, color=line_colors[label])

ax2.set_xlabel('Month (Since Aug 2016)', fontsize=20)
ax2.set_ylabel('Success Rate (%)', fontsize=20)  # Replace with your actual Y-axis label
ax2.tick_params(axis='both', labelsize=20)
ax2.set_title('Reproduction and Fix Location Success by Month', fontsize=20)  # Replace with your actual title
ax2.legend(loc='lower right', fontsize=20)

# Adjust layout
plt.tight_layout()

# Show the figure
# plt.show()
plt.savefig("./DatasetGrowth.pdf")
