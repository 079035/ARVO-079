# Focus on Modification rather than number of file that are modified
1. We are going to send the original code to the Codex rather than a file.
2. If we use n>1 to get more than 1 fixes from Codex and try to verify all of them, the time complecity is `O(n^m)` assuming there is `m` different modificaitions in one file.
3. Could we test all of them?
  - For most cases, `m` is small
  - Set the max value of n^m
  - For the fix that has big m, most modification are not bug-related. AKA, (bad habit) combine tons of commits in one commit.
  
  
# Carper
1. Use the diff file and github commit message to build the module
2. Has high success rate(30%-55%) for 4-Parity cases



# Success Rate after fixing bug

5.3%

# New Idea
Get the information from the fix.
- Provide what function should be used
- Provide what varible should be used
