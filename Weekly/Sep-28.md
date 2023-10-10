# Lat Week
- Have enough report and know how man fixes are only related to single file.


- Add patch_info to the report


# Last Week
- Test how large will the image be if we commit the container as an image
    - Test Case 1: Project freetype2 and small_libexif ~= 1.75 GB 
    - Test Case 2: cblosc2 3.75 GB
- Speed Up report generator
    - Hard to speed up
        - Example, there are 130 issues I need to compile [2,8] times to find the fix
        - Every compilation takes 5 mins
        - We need 30~40 mins to generate one report
        - We have 1000+ issue which may take 500+ hours(1 month)
    - A way to speed up (in testing)
        - Multi-thread, current work load is about 10/128
        - But sometimes, it fails to build the binary under multi-thread mode
        - Fixing the bug...
- Report:
    - More info
    - Question: Patch Info: should we attach the diff file?
