# Paper Reading, DiverseVul
- Their main work is building a new dataset
  - I didn't find any links to the dataset
  - It includes vulnerable/not vulnerable **functions**
- Their work summary is helpful
  - It's difficulty to generalize the model
  - we'd better use code-analysis-related pre-trained model

- The size of their dataset ~= current oss fuzz dataset
- Their target also includes identifying (vul/not vul) functions while our is classify the vulnerablities.
- I need to read their experiment part again to get more information


# Our project
- OSS-Fuzz is strong, big, and growing
- Grab data from OSS to build a growing dataset is an important part of our project
- But now it's difficult to show that our dataset is influential since we have difficulty to
  - show that we can verify autofixers' fixes
    - Compromised solution: label it manually and assume in the future we'll have a ML model do such work
- Not reproducible data is also important, since it's great source of ML. And the source of ML is very important.


```
- If we have a model to classify the vulnerability
->We can label all OSS Fuzz data
->Use the generated information to generate helpful prompt 
->Help people to fix/ Generate a mild fix
```
But it's hard now. So we can target on building a dataset so people can train their models.