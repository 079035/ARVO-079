import matplotlib.pyplot as plt
from collections import Counter
import glob
import json

meta = Counter()
for f in glob.glob('../../../Reports/*.json'):
    js = json.load(open(f))
    proj = js['project']
    meta.update([proj])

# Assert counts are the same
for k in meta.keys():
    assert meta[k] == meta[k]

total = sum(meta.values())
labels_projects = []
sizes_projects = []

for key, val in meta.most_common(10):
    labels_projects.append(key)
    sizes_projects.append(val)
labels_projects = ["Other Projects"]+labels_projects
sizes_projects  = [total-sum(sizes_projects)]+sizes_projects

langdata = Counter()
for line in open('project_langs.txt'):
    langdata.update([line.strip().split()[1]])
labels_langs = [ x[0].title() for x in langdata.most_common()]
sizes_langs = [ x[1] for x in langdata.most_common()]
print(labels_langs)
print(sizes_langs)

colors = [
    '#1f77b4',  # Muted blue
    '#ff7f0e',  # Safety orange
    '#2ca02c',  # Cooked asparagus green
    '#d62728',  # Brick red
    '#9467bd',  # Muted purple
    '#8c564b',  # Chestnut brown
    '#e377c2',  # Raspberry yogurt pink
    '#7f7f7f',  # Middle gray
    '#bcbd22',  # Curry yellow-green
    '#17becf',  # Blue-teal
    '#aec7e8'   # Soft blue
]
additional_colors = [
    # '#f7b6d2',  # Pale pink
    '#98df8a',  # Light green
    '#c7c7c7',  # Light gray
    '#dbdb8d',  # Olive green
    '#9edae5',  # Soft cyan
    '#ff9896',  # Soft red
    '#c5b0d5',  # Lavender
    '#c49c94',   # Dusty rose


]
#% Language distribution
#%{'c++': 171, 'rust': 3, 'c': 50, '': 3, 'python': 2, 'swift': 2}
#% {'c++': 0.439588, 'rust': 0.05172413793103448, 'c': 0.4098360655737705, 'python': 0.007633587786259542, 'swift': 0.666666 <- only 2/3}

explode = [0.2]*len(labels_projects)
explode_gender = [0.05]*len(sizes_langs)
#Plot
# print(len(sizes),len(labels),len(colors))
plt.figure(figsize=(20, 12))  # Width, height in inches


plt.pie(sizes_projects, labels=labels_projects, colors=colors, startangle=70,frame=True, explode=explode,radius=3,textprops={'fontsize': 30})

plt.pie(sizes_langs,  labels=labels_langs,colors=additional_colors,startangle=175, explode=explode_gender,radius=2,textprops={'fontsize': 24})

# plt.legend(loc='lower left')

# plt.legend(labels=labels_years, loc='best')  # Adding legend

 # Positioning the legend in the lower left
#Draw circle
centre_circle = plt.Circle((0,0),1.5,color='black', fc='white',linewidth=0)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.axis('equal')
plt.tight_layout()
# plt.show()
plt.savefig("./Distri.pdf")
