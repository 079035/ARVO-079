import matplotlib.pyplot as plt
import numpy as np

# with open("./16k.log") as f:
#     lines = f.readlines()
# d = {}
# import json
# for line in lines:
#     item = json.loads(line)
#     key = int(list(item.keys())[0])
#     val = list(item.values())[0]
#     d[key]=val
# from collections import OrderedDict

# # Sort the dictionary by key and create an OrderedDict
# sorted_dict = OrderedDict(sorted(d.items()))

# print(sorted_dict)
# res = []
# for x in sorted_dict.keys():
#     if sorted_dict[x]:
#         res.append(1)
#     else:
#         res.append(0)
import matplotlib.pyplot as plt
import numpy as np
import json
# Example data: Replace these with your actual lists
with open("round2.json") as f:
    dt = json.loads(f.read())

lists = []
for x in dt.keys():
    lists.append(dt[x])


# ... similar for list3, list4, list5, list6
# lists = [list1,list2]
# Converting boolean lists to numerical lists
res = []
for l in lists:
    tmp = []
    ct = 0 
    for x in l:
        if x:
            ct+=1
        tmp.append(ct)
    res.append(tmp)
# Creating a new figure
plt.figure(figsize=(12, 6))

# Adding step lines for each dataset
x = np.arange(100)  # Assuming all lists are of the same length (100)
keys = list(dt.keys())
print(keys)
order = ["gpt-4","gpt-3.5-turbo-16k","gpt-3.5-turbo","Codex","Wizard-34B","Wizard-15B","Starcoder"]
labels = ["GPT-4","GPT-3.5-turbo-16k","GPT-3.5-turbo","Code-davinci-edit-001","Wizard-34B-V1.0","Wizard-15B-V1.0","Starcoder"]
for name in range(len(order)):
    i = keys.index(order[name])
    lb = labels[name]
    plt.step(x, res[i], label=lb)

plt.title('AI Model Benchmarks',fontsize=20)
plt.xlabel('Case Index',fontsize=20)
plt.ylabel('Fix Success Rate (%)',fontsize=20)

# Adding a legend
plt.legend(prop = { "size": 15 },)

# Show the plot
# plt.show()
plt.savefig("./Evaluation.png")