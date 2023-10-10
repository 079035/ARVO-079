# Statistic

## Sanitizers

For 571 reports, there are .
```s
asan:            359
ubsan:           70
msan:            142
```

They can all provide backtrace information. 
Since more than half of reports use ASAN, I wrote a ASAN result parser to get the back trace information first.
If it's helpful, I'll implement result parsers for ubsan and msan.

The following result is the asan parser result, which tells us how many modifications 
are in the same function where crashes happen.

Asan sanitizer paerse is finished but I made a mistake and 
lost the data so it's still running to get all backtraces 
of crashs.


For C++ program, most modification are not in the same 
place the crash happends so I back trace 3 functions(or we need to trace more). 


## get_fix_meta

The fix metadata is in file fix_meta.
I found 
- Most cases only modify one or two files
<<<<<<< HEAD
    - Modify one or two files: 313+127/569
    - Modify Two files: 127/569
=======
    - Modify one file: 313+127/569
    - Modify two files: 127/569
>>>>>>> 6655141738e106fe7957b479b8bf044490f9021a
- 37.26% cases modify one place in one file
    - Modify one file and only one modification is found: 212/569
- Data of lines added or moreved is also in the result

# Analyszed Vulnerability Summary

Try to finish this task asap.
