import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt
import numpy as np
import json
# Example data: Replace these with your actual lists
res = []
for x in range(5):
    with open(f"{x+1}.json") as f:
        tmp = f.readlines()
    assert(len(tmp)==100)
    d = {}
    for x in tmp:
        obj = json.loads(x)
        num = list(obj.keys())[0]
        d[num] = obj[num]
    x = {key: d[key] for key in sorted(d)}
    res.append(x.values())
rrr = []
xxx = []
for x in res:
    tmp = [] 
    for y in x:
        if y==True:
            tmp.append(1)
        else:
            tmp.append(0)
    xxx.append(tmp)
for x in xxx:
    print(sum(x))
for x in range(100):
    ct = 0 
    for i in range(5):
        if xxx[i][x]:
            ct+=1
    
    rrr.append(ct)
print(rrr)
exit(1)
rrr = [] 
for x in res:
    ct = 0
    tmp = [] 
    for i in x:
        if i==True:
            ct+=1
        tmp.append(ct)
    rrr.append(tmp)
res = rrr






plt.figure(figsize=(12, 6))



# res = rrr
# Adding step lines for each dataset
x = np.arange(100)  # Assuming all lists are of the same length (100)
# keys = list(dt.keys())
# print(keys)
order = ["Round1","Round2",""]
for i in range(5):
    lb = f"Round {i}"
    plt.step(x, res[i], label=lb)

plt.title('GPT-4 multiple Rounds Evaluation',fontsize=24)
plt.xlabel('Case Index',fontsize=24)
plt.ylabel('Fix Success Rate (%)',fontsize=24)

# Adding a legend
plt.legend(prop = { "size": 24 },)
plt.tight_layout()

# Show the plot
# plt.show()
plt.savefig("./G5.png")