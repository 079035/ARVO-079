# OpenAI Codex/ Auto Fixer Framework
- Implement the framwork to apply and verify the fixes in scale
    - Get the vulnerability info from report, including vul_commit, fix_commit, diff_file, and vul_type
    - Get the vulnerable code and the line number of vulnerability in diff_file 
    - Use vulnerability type + vulnerability position to generate fix instruction*
    - Send to the auto-fixer and apply the result to the code
    - Use the fixed code to build a binary and verify it with Poc
    - Report the auto-fixer's fix and the real fix so we can verify the fix
- The code is in file ../fx.py

## Question
- How can we give better instrcutions
    - For example,  
    - 46309 (Hard to give right instruction)
    - 45884 (Werid Fix/ Bad Fix)
    - 40431 (verible is far away)
- I find if I only give very short code segments (about 10 lines), Codex almost can't fix it(only few successful cases).

# Unsatble Cases
- Find some unstable cases and cleaned them in issues

# TODO
- Even it shows that the fix works, I find that the Codex would just return the function so the Poc can't trigger the vulnerability. So we need to check functionality
- Insert Mode is on the way, we already have a framework, what we need to do is implement the API call.
- BETTER INSTRUCTIONS!