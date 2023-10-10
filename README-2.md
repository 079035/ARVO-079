# Stage2

I added several new features to this project. And solved several sticky issues.

# Problem

In the real world, it would take weeks to fix a reported vulnerability and the fix-confirm report would also take weeks.

This fact results in that we can need to find the fix in hundreds of commits which may be related to thousands of modifications. 

It's a hard challenge for implementing our other idea. 

- First, if we can't know where the fix is we also can't know where the vulnerable code is. So we can't summarize the existing vul and find more vul in other projects.
- Second, we can't just tell the auto fixer "Hey buddy, there is a vulnerability in the repo. Please help me fix it.". We should tell the fixer where exactly the vul is
- Third, if we want to improve the auto-fixer, we need plenty of fix-examples in real world
- ...

So I think this work would be meaningful!

And based on our previous work, I have an idea!

# How to locate it?

Based on the last update, according to google's oss-fuzz public bug info, We can now compile a vulnerable version binary with or without spesific vulnerability. 

According to oss-fuzz's bug report, We know the commit where the vulnerability is reported and the commit where the vulnerability is already fixed.

But we can't know the commit when the vulnerability is exactly fixed. But luckily, with our previous work, we can make it!

The basic idea is the dichotomy:
- We are able to build the fuzz targets at a specific commit.
- Assume 
  - we have a list of commits: `[c1,c2,c3...,c132]`
  - we can compile them to fuzz targets: `[f1,f2,...,f132]`
  - `cx` is the commit when the vulnerability is fixed
- So we could build and test fuzz target `fx` to test if it could trigger case with our poc 
- until find the `cx` where `f(x-1)` crashes and `fx` doesn't crash
- commit `cx` is the commit that fix the vulnerability

# Testing

The coding part is finished. 


We need to test more and fix the bugs.

# What's Next

We could use this to build kinds of datasets, such as 

- vulnerable code pieces database
- fix code pieces database

We can use these data to

- test/train auto-fixer
- find more similar vulnerability


All of our data comes from the real world so we could get something valuable from it!
