import json
with open("16k.log") as f:
    liens = f.readlines()
d = {}
for x in liens:
    item = json.loads(x)
    key = list(item.keys())[0]
    d[int(key)] = item[key]
sd = {k: d[k] for k in sorted(d)}
# print(sd)

page = int(1377//3)
keys = list(sd.keys())
res = []
for x in range(3):
    tmp = [] 
    ct = 0 
    for y in range(page):
        if sd[keys[x*page+y]]:
            ct+=1
        tmp.append(ct)
    res.append(tmp)
# print(res)



import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(projection='3d')

colors = ['r', 'g', 'b']
yticks = [2017,2020,2023]
ct = 0 
for c, k in zip(colors, yticks):
    # Generate the random data for the y=k 'layer'.
    xs = np.arange(page)
    ys = res[ct]
    ct+=1 

    # You can provide either a single color or an array with the same length as
    # xs and ys. To demonstrate this, we color the first bar of each set cyan.
    cs = [c] * len(xs)
    cs[0] = 'c'

    # Plot the bar graph given by xs and ys on the plane y=k with 80% opacity.
    ax.bar(xs, ys, zs=k, zdir='y', color=cs, alpha=0.8)

ax.set_xlabel('Case Index',fontsize=16)
ax.set_ylabel('Timeline',fontsize=16)
ax.set_zlabel('Fix Success Tally',fontsize=16)

# On the y-axis let's only label the discrete values that we have data for.
ax.set_yticks([2017,2020,2023])

plt.show()
# plt.savefig("16k.png")