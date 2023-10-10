# Fix the issue which leads to failure last week

Because Google set the oldest image to " 0082022e1c5b   —   Dec 31, 1969" on Oct 1, 2022.

So the old issues would fail to build.

# Make Issues More Reproducible

- Build Docker images and store it
    - Build the old without removing the container
    - Commit the container
- To make reproduction more stable

# Manually Fix the vul with Codex
- There are only a few easy (UAF, Off-By-One) cases
- How can we fix complex cases?
    - They have different vulnerabilities
    - They have multi-fixes, such as adding a variable...
- Generating good instruction is the most challenging problem.
