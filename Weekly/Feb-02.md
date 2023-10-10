# Statistics

For our reports, we can quickly (10min/500+ reports) get the statistics of the patches, including
- How many files are included
- How many lines are added/modified

There are some metadata for 556reports:
- 56%(309/556) patches are only related to 1 file
- 23%(130/556) patches are only related to 2 files
- 21%(117/556) patches are related to more than 2 files


The numbers of added/removed lines are also attached in this [file](../Data/_fix_statistics.json).

# Fix a critical bug
- Which results in returning the wrong vul code.
- More tests are needed. 

# Codex Part
1. Doing: Modify the code + recompile
    - Use Codex to generate n completions with different temperature/prompt
    - Build the first one and verify with keeping the container alive
    - If fixed, return True
    - Else, 
        - modify the code and recompile 
        - It's Faster, cuz we don't need to build the image again, and partial dependencies are compiled)

2. Question: Can we get a simpler dataset for testing
    - Because we are trying to find a good strategy and current dataset is big and complex
    - The real-world dataset is too hard and we can't see the difference
    between different strategy
    - The oss-fuzz data is not labeled so it takes time to analyze "why can't we fix it"
    - If we have a simpler dataset to find a useful strategy, we can later 
    test it on our dataset(OSS)
    - Write it ourself(may 20 classical cases) or what do you recommend?


# Other Issue

## The /data folder is full

```
33T     /data/rkant
```

## Is OpenAI slower?

In the testing, I found it takes a long time for going through all reports.
The time increased to 1 hour from 30 mins.