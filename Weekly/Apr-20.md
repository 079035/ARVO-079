# Main Challenge
Evaluate Codex: Unable to generate helpful instruction for Codex
```
- Unable to label OSS-Fuzz generated cases to tell what kind of vulnerability it is
   - Build a Machine Learning model to distinguish different types of vulnerabilities. (Hard)
   - Use other people's tools (I have one idea in the "New Idea" section)
```
Implementation:
```
- How do we know the modification is related to functions/global variables out of the vul functions?
  - Should we parse patches and get the name of functions and global variables?
  - Is binary a better target? (we only need to focus on `call` and instructions related to `RIP+?`)
```

# New Idea

- Can we use chatGPT to generate the prompt based on the patch to label our dataset?
- Basically, this method is used to solve the problem that I don't have enough experience to build a specific classifier/ML model. I use ChatGPT and assume I could build a more specific ML module.
- For example, I want to test "If we have a better/more detailed prompt, Codex can fix the real world vulnerabilities"
- Case study: Easy OOB
  - Choose an issue: 40508, more information about the issue is at [this file][2]
  - Mually analysis: This is a bug that could lead to OOB access `if len ==0, utc[-1] is OOB`.
  - And I get the following patch [description][3] from ChatGPT
  - After I got the patch description, I used this [script][1] to ask Codex to fix the vulnerability but failed
  - I tried to manually fix the prompt but can't stop Codex from checking the variable before we assign it!
- More tests are needed but the result should not be good according to my test result.


# Paper Scope
Do we focus on the dataset (evaluating codex) / (coming up with a new ML method to make vulnerability fixing easier) or both?

If we focus on the dataset, we need to do more work on the dataset's features. Design experiments to show people the novel features of our dataset and compare our dataset with others. We can do the work as follows:
  - Show the growth of the dataset in past years
  - Show the reproduce-success rate for different time
  - Compare the features/size with other datasets

If we focus on the ML part, my current point is that Codex doesn't have the ability to provide a useful fix for 
real-world security issues. But we can still show people our findings. The difficulties we encountered. Also, our experience would be helpful to other people doing similar research.



[0]: https://github.com/net-snmp/net-snmp/commit/c6b84c8fdb0a6847f7691201be2e36e155c6e22d
[1]: ./Exmaples/davinci-fix.py
[2]: ../Reports/40508.json
[3]: ./Figures/Figure1.png