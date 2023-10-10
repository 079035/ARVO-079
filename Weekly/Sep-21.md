# Last Week
- Report Module
    - I run the project on the server after solving lots of bugs, including
        - Wrong timezone setting bug, cuz the server is at UTC
        - Srcmap Order bug, I assumed the result of Path glob is at the correct order(dictionary order)
    - Implemented the report module
    - Dry run the report module for 12 hours
    - Get 24 report samples
    - Analysis some of reports and find it works properly
    
- Run the reproducer module and have some interesting findings
    - There are more than 9000 new issues in last 10 months
        - oss-fuzz's output is increasing!
        - Our database is increasing!
    - Our project has better performance in recent issues(40000+)
        - That's may because
            - all the dependencies of these new issues are avaliable
            - The developers are going to write better build file
        - Should we keep meticulous to the new reproducible issues?
            - people may not be able to reproduce these issues after 6 monthes if the main reason is reason1
            - People are able to reproduce these issues if the main reason is reason2

-  AI test
    - Test some simple test case manually
        - Find some smart fixes, such as 3447
        - Find some stupid fixes, such as 11429
        - Find some cases that are hard to fix, such as 5761

# Next Week
- Have enough report and know how man fixes are only related to single file.
- info from the ori report: asan/... fuzzername 
- Add patch_info to the report