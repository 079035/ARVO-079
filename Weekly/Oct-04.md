# Issue1 - Fixed
It's hard to find the real fix of some issues such as 8333 
even if we are able to reproduce the fix and the vul.
The reasons is it's hard to find which repo is vulnerabile code in.
For example,
```
{
  "/src/libqxp": {
    "type": "git",
    "url": "git://gerrit.libreoffice.org/libqxp",
    "rev": "6c9733fedff83af21b2218012e3c7c51ea3710d6"
  },
  "/src/libetonyek": {
    "type": "git",
    "url": "git://gerrit.libreoffice.org/libetonyek",
    "rev": "935cb58a61e45f441bdea143317a7d0d52c7f944"
  },
  "/src/libabw": {
    "type": "git",
    "url": "git://gerrit.libreoffice.org/libabw",
    "rev": "0eb2512fd9b81bafcb8bcf23ef02a6818d0c4b81"
  },
  "/src/libe-book": {
    "type": "git",
    "url": "git://git.code.sf.net/p/libebook/code",
    "rev": "1542c489376defef98ec61047ff434bff0bbe83a"
  },
  "/src/libmwaw": {
    "type": "git",
    "url": "git://git.code.sf.net/p/libmwaw/libmwaw",
    "rev": "22aa6f6b0f38c40bf20fd21ea4023245ead68af0"
  },
  "/src/libwps": {
    "type": "git",
    "url": "git://git.code.sf.net/p/libwps/code",
    "rev": "b8897585d4ffa503d88c98b31fbb5b7ccc2a01cd"
  },
  "/src/libstaroffice": {
    "type": "git",
    "url": "https://github.com/fosnola/libstaroffice",
    "rev": "6cf476b7449831d340ec54bd87d653d53209a0cf"
  },
  "/src/libwpg": {
    "type": "git",
    "url": "git://git.code.sf.net/p/libwpg/code",
    "rev": "a91d803f2878c9b6eb244fbcf9597e6fe236bdad"
  },
  "/src/libwpd": {
    "type": "git",
    "url": "git://git.code.sf.net/p/libwpd/code",
    "rev": "f1a6690683c80ea4e401920c7ef0ba11d4fef98c"
  },
  "/src/libfreehand": {
    "type": "git",
    "url": "git://gerrit.libreoffice.org/libfreehand",
    "rev": "2902e26b98635d750f053acca9c338feb7fe7ea8"
  },
  "/src/libpagemaker": {
    "type": "git",
    "url": "git://gerrit.libreoffice.org/libpagemaker",
    "rev": "4af124c8f6205236e9fb9882203be5f8115e3dd2"
  },
  "/src/libzmf": {
    "type": "git",
    "url": "git://gerrit.libreoffice.org/libzmf",
    "rev": "a2840fa8ce65f7c2e2b9b5679387f4e1ff59947e"
  },
  "/src/libvisio": {
    "type": "git",
    "url": "git://gerrit.libreoffice.org/libvisio",
    "rev": "c1bb49486e73e9e19944be6a995e3bbd96210f8f"
  },
  "/src/libcdr": {
    "type": "git",
    "url": "git://gerrit.libreoffice.org/libcdr",
    "rev": "93f8e7405e4a852a2908c011456719dc8e3033e6"
  },
  "/src/libmspub": {
    "type": "git",
    "url": "git://gerrit.libreoffice.org/libmspub",
    "rev": "3988aba06f5297fc2262462d89cb601aeffcae3b"
  },
  "/src/librevenge": {
    "type": "git",
    "url": "git://git.code.sf.net/p/libwpd/librevenge",
    "rev": "19c411a48f12404b1a5eb323ba42dacb145ad06c"
  },
  "/src/libfuzzer": {
    "type": "svn",
    "url": "https://llvm.org/svn/llvm-project/compiler-rt/trunk/lib/fuzzer",
    "rev": "332082"
  }
}
```

The fix:

After reviewing lots of cases with this issue, I find we can just assume the first item is the target repo.
It can solve  about 70+% cases in testing.

# Issue2 - Are we using the correct and precise srcmap?

tl;dr -> Yes

- I read the code and find Prof. uses bucket to download the json file(BDG.py - line 355). The target address is "clusterfuzz-builds-afl/gdal/gdal-address-201803020649.srcmap.json" which shows we download the srcmap from the 
correct place. 
- To verify the previous point, I used gsutil to download skia's srcmap and compare it to our local version. The result shows they are the same. (gs://clusterfuzz-builds/skia/skia-address-201801232054.srcmap.json)

# Task - Report
- We have 485 reports now and it's increasing.

- Issue1 is just fixed so we are going to have about 100+ new issues.

- I would find and fix other issues to make the number closer to the 
number of our reproducible issues.


# Question - Move Docker Data
Now I am runing the docker with cleaning some of the images. 
And I read some data move articles and consider to move docker dir to 
"/data" so we can test to pack the commit to image and make reproduction 
easier.

- Is /data SSD or Disk? 
- If /data is disk and we want to keep the speed of docker, is there anyway to just change the configure file to let docker use several 
dirs to store images.


# Question - Codex 

- It's 500 reports a good number of dataset to start codex part?
- What's the first step to evaluate codex or What kind of data do we need to confirm the next step 