# CVE Filter
- Only include c/c++ based CVEs
- 663 cases left

# Visualize CVEs based on their CWE type
- The result in [this dir](../DYE_CVE/)
- The result shows the vectors can't show the difference between different CWE cases
- It may not be feasible to use source code's embedding vectors to predict its CWE type

# Finding in the test
- Before I filter other language CVEs(py/PHP), I found the vectors recognize the different languages.
  - For example, c language and PHP language
- So I think the format is an important part to generate the embedding vectors.

# Thoughts

- Codex should understand the meaning of the code but the result shows that it's hard to recognize the difference between vulnerable code and secure code
  - The difference between vulnerable code and secure code may be too tiny to recognize 
  - The data, used to train the embedding module, focus on other parts more than the code
  - Possible solution: have a module that can better extract the features of source code
- What if we use assembly language to generate the vectors
- Not sure if it makes sense
  - Pro: Decrease the influence of the coding habit, and code format and focus on the code itself
  - Con: The input would be too long to handle. It's hard to test this idea since more infrastructure stuff is needed.

# Classifier
- Focus  too much on the CWE result and didn't start it
  - Don't believe the result and debug it for a long time
  - According to the Visualization result, does it make sense to build the classifier based on the vectors of the source code?