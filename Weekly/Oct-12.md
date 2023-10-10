# Move Docker Data

- We need to store two different images, the vulnerable image and the fixed image.
- How would people use these images, assuming that we public them and people can download it.
    - They use these images because they have trouble with using our reproducer and the reasons may be
        - 1. Can't download the file or resource in dockerfile, for example 'curl the source of a dependency'
        - 2. Github Project is moved to somewhere else, for example, svn
        - ?
    - They would run the docker images, use their fixer to fix the code, compile the code, and test with the testcase.
- What are needed?
    - Source code of dependencies
    - and ?
- How to implement?
    - Compile and verify once (Make sure it's reproducible)
    - commit to two images: the vulnerable one and the fixed one
- It can be complex, I think we'd better to focus on codex part and commit all reproducible cases to image with ignoring some bad cases in them

# Add More Issues to Dataset

- Clean all rest issues mainly including projects only have few cases
- Remove not reproducible cases that were able to reproduce two months ago
- Finish this part and focus on Codex


# What I did last week
- Code for move data data (Not finished)
- Clean old issues, now we can focus on new issues/other parts
    - Try to reproduce it and make a image
- OpenAI
    - Analysis the reports
        - How many files are related to the fixes
        - How many lines does the fix insert, modify,and remove
        - What's the vulnerability
    - Play with playground
    - Examining Zero-Shot Vulnerability Repair with Large Language Models
    
        