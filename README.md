# oss-reproducer
This work could reproduce the `Bug-Security` issues of oss-fuzz. 

You can:
1. Build a database to test your auto patcher.
2. Reproduce certain vulnerable binary.
3. Build your own vulnerability database for other research
...

# Usage

I mainly run the oss-reproducer on windows-wsl, and for MAC users, I highly recommend you "DO NOT" run the oss-reproducer on MAC, because the `-v` docker parameters, it's super super slow to run the compilation on MAC docker. I tried MAC-VMware-Ubuntu, and it could work. 

Btw, I recommend you to use virtual-env of python3.

## Basic Setting

Creat `_profile.py` to init your setting. Example:

```python
gcloud_key    = '/mnt/c/Users/n132/Documents/GitHub/OSS-Fuzz-Constructor/oss-pro-key.json'
oss_fuzz_dir  = '/mnt/c/Users/n132/Documents/GitHub/oss-fuzz/'
reproducer    = '/mnt/c/Users/n132/Documents/GitHub/oss-reproducer/'
DATA_FOLD     = 'Type.Bug-Security_label.Reproducible_status.Verified'
outdir        = '/tmp/oss-out/'
workdir       = '/tmp/oss-work/'
Debug         = False
TIME_ZONE     = -4
```
- oss-pro-key, the oss resource is on gcloud, you need to modify your key's location
- we need some functions in oss_fuzz_dir, I have almost implemented them in my version, but I think there are still some left
- reproducer, oss-reproducer 's address.
- DATA_FOLD, you can init it by using BDG's script, it would contain the srcmap and a database of security-bug issues
- outdir, the fold to store the compiled fuzz-targets
- workdir, the fold to store the compiling fuzz-targets
- Debug, legacy button, you can keep it False
- TIME_ZONE, your time zone.

## Setting

There are some important global settings in the `untils.py`. You can keep most of them.

CLEAN_TMP, set it to `False` if you want to debug so the local file would not be deleted. So you can copy the commands during the building, such as `docker run .....` to reproduce the crashes. And remember to set it to `True` when testing. Btw, the memory leak still exists, but not too much. You need to clean the tmp file in `/tmp`.

Also, we need to clean the disk periodically, because the docker would not shrink its disk on windows. You need to shrink it manually. Besides, you can run turn on "FORCE_CLEAN", it would run clean command periodically, which is similar to `docker rmi $(docker images --filter "dangling=true" -q --no-trunc)`. But I don't recommend you do that, because it would make the building extremely slow. For manually clean, you only need to run it when the docker runs out of your disk. If you are working on Windows, you can use the following script in PowerShell(admin) to shrink the wsl and docker.

```s
# Clean Docker
docker system prune -a -f
net stop com.docker.service
taskkill /F /IM "Docker Desktop.exe"
wsl --shutdown
Optimize-VHD -Path "C:\Users\n132\AppData\Local\Docker\wsl\data\ext4.vhdx" -Mode Full
wsl
net start com.docker.service
#---------------------------------------------------
wsl --shutdown
diskpart
# Clean WSL
select vdisk file="C:\Users\n132\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu20.04onWindows_79rhkp1fndgsc\LocalState\ext4.vhdx"
attach vdisk readonly
compact vdisk
detach vdisk
exit
```

OSS_DB_MAP, you don't need to change it but it's worthy to mention it. It would store the repos, it can accelerate the build. But it would cost lots of memory if you run oss-reproducer for a long time (e.x. 6 months). You can securely `rm` the whole dir. It would init and grow automatically.

## Windows/Linux

I would not verify all the issues at one time, because it would take years! There are two common uses.

1. Play with a certain issue, verify the crash and the fix; play with issues from the same project

```s
# play with a issue
python cli.py <issue_number>
# play with a project
paylon cli.py <project_name>
```

2. More hardcore testing/debugging, modify the `unitTest.py` and implement your own test. I don't have time to write a document for the functions. If it's needed in the future, I would write that. You know, I am not a programmer, my coding is awful, I even don't want to read it again.


# Targets
We have 6992 issues. (Feb-2022)
6913 of them have more than 0 scrmap.(>0)
6318 of them have more than 1 scrmap.(>1)
These 6318 issues are our target.

4686 of them have less than 5 dep(<5)
My first stage work focused on these relatively simple issues.




# Performance

[Result Details](./Results.json)

The reproducer could handle simple cases, around 1024 cases are verified. I have played with this reproducer for about several hundreds of hours. I really like simple projects. The word "simple" doesn't mean the dependencies (if there is no any lost in srcmap), but mainly the builder. Sometimes the dockerfile also matters.

What's a yummy builder? You can check all the builders in [oss-projects][1]. Take an example, the project `binutils`, it's a very complex project. It may take hours to compile a single issue and its `build.sh` is very complex but the most important thing, it's time time-independent-code (I invented it, lol, a concept similar to PIC). It would not download the dependencies in `build.sh` I can surely tell you I find there is a "git clone" in `build.sh` so many times. That's the nightmare of me and the reproducer. Because, We can't get the revision of the dependencies in `build.sh`, such as issue `34927`. In my view, the current reproducer could get about 1500 issues without much modification. The log part is really important in one way, you can focus on the not tested part to expand the reproduce database, in another way, you can focus on the failed issues to improve the oss-reproducer. 

For the first way, you can focus to test untested little projects. There are around 1200 little projects currently. I call them little projects because each of these projects only has less than 17 issues. You can check their name in `RRYS@unitTest.py`. I did a simple test on the first 80 cases and found that around 1/6 of them are reproducible with the current version of oss-reproducer. Besides, the big projects,


I'll talk about several issues I know. Solving them could also expand the reproduction database. But I suggest you start with easy projects! 

# High-level workflow

- Take the `localID` of the vulnerability
- Find the corresponding `srcmap`
- Download certain version dependencies
- Build the vulnerable fuzzer targets
- Test the vulnerable fuzzer targets to trigger the crash
- Build the fixed fuzzer targets
- Use the same crash_input to verify the fixing 

# Workflow
- Handle bad issues
  - Don't have a reproduce_case
  - Don't have a project_name
  - Don't have a srcmap/ have a broken srcmap/ have more than two / only have one
  - Don't give a fuzzer_target name
- Parse the srcmap to get the dependencies, include their URL, revision, and type 
  - Some links can't work now
    - when the repo is moved to git, we use a transfer to get the correct link.
    - (Todo) svn to git, we need to use git-svn to get the correct revision
    - (Can't solve) we lost some repo permanently
    - (Todo) llvm project is a big problem, it is one of the dependencies of any project. I used a simple way(use the latest oss-base-builder which includes the latest lib-fuzz) now but it doesn't work well.
- Use Git/hg/svn to download code and checkout to the specific reversions
- Checkout oss_fuzz/project/XXXX to the latest revision before the reported bug
  - Get the date of the bug_revision
  - use git log to get the latest revisions of dependencies
  - check out
- Find the latest oss container before the bug's reported time 
  - Use gcloud API to find the latest revision
- Modify the dockerfile
  - (Todo) It's too slow to download all the dependencies during the build, that's redundant, we did that during parsing the srcmap file.
  - (Todo) add `git config --global http.sslverify false`
  - add `apt update`, because some bad dockfile don't have this step
- Handle bad build.sh (Hard)
  - (Todo) Some build.sh would run `git clone` / `svn co` / `hg clone` so that we can't get the right version dependencies.
  - (Can't solve) Curl/wget link can't work
  -  It's part is my nightmare when dealing with large projects. They have tons of dependencies in build.sh. And I need to check to build.sh(they are even different on different revisions!). That really takes time.
- Rollback mechanism
  - Checkout back to the master
  - Delete corrupted docker image
- Tmp_dir/image clean mechanism
  - In debug mode, we need these folds to help us to reproduce the bug
  - But in bundle test mode, my disk would be filled soon.
  - Clean `None/None` images 
- Signer/bundle/project verifier
  - Check if the `old fuzzer_target + reproduce_case` would get a crash
  - Check if the `new fuzzer_target + reproduce_case` wouldn't get a crash
  - This step really takes time, some projects need >1hour to compile. Don't use them to test! 

# Tipical Bad Issues

I'll attach some super bad issues/projects here so that you can 

1. fix these issues
2. Stop wasting time on these issues
3. Learn to write a good build.sh/Dockerfile for your project 


```s
## 0x01
26 issues in sqlite3
Use curl in dockerfile to download the code, so we can't get the revision. Bad project!

## 0x02
Issue 34927
1. It copies build.sh from the repo, we have to modify the dockerfile
2. `git config --global http.sslverify false`
3. It uses git in build.sh! We can't deal with this now because we don't know the revision of these deps and it's a super big project to modify the build.sh to make sure all the dependencies are at the correct commit.
4. Can't compile for some reason, I don't want to solve this issue before solving the previous one. because they may be related.

## 0x03
Issue 42950, freetype2
It builds a wrapper, so we need to change the buildfile to get the correct revision
```

# Todo

I solved tons of issues/bugs. However, there are tons of tons of issues/bugs to be solved. I list the issues I know. If you would like to help, thanks to you so much for your PR!

- Time
  - TimeZone: This project now needs to change the Timezone manually in `untils.py`. It would influence the oss_container's version. It's better to make it automatically.
  - More Precise Timestamp: Now I choose the oldest dependency's revision timestamp as the time limit of the oss-reproducer. It's imprecise, we can improve this part to expand the reproducible database.
- More hg and svn support
  - I focused on `git` projects. There is poor implementation of `hg` and `svn`.
- Mark 100% unreproducible issues
  - Some cases can't be reproduced anymore for some reason( unaccessible dependencies). We need to mark it as unreproducible to avoid more time waste.
- git SSL verify
  - Sometimes the git pull in dockerfile would fail without setting `git config --global http.sslverify false`. I don't have a good way to fix it now, maybe we can insert that command to every dockerfile. I didn't test this solution yet because I worried that would lead to more issues. If you know this verification mechanism well, please help me fix this issue.
- More complete crash log
  - The current crash log could only show where the crash happens during the building. We can make it show more details. It's really helpful to people who want to reproducer and improve oss-reproducer.
- Prune Dockfile before building
  - It's too slow to download all the dependencies during the build, that's redundant, we did that during parsing the srcmap file. We can find these commands and remove them. 
  - For some dockerfile, inserting `apt update` is necessary but for others it's redundant. I used a simple solution and added `apt update` to all the dockerfiles. It's simple but would lead to meaningless time-consuming. Please fix that if you have time and experience with `regular expression`.
  - In some bad dockerfiles, it would download some dependencies by curl or wget. Unluckily, these dependencies can't be recorded on oss-fuzz's srcmap. Also, these bad dockerfiles would also fetch some resources by curl/wget, and these resources no longer exist. I have no idea about these issues. 
  - The rest bad dockerfiles, I promise you will see kinds of awful dockefiles!
- The verifier
  - I only simply run `fuzz_target crash_trigger` and check the `$?` locally(on wsl).
  - It's obvious that the environments are different. it's better to run the `fuzz_target` in the corresponding container. During my test, I found some `fuzz_target` can't run properly on wsl because of `lib not found issues.
  - Most times `$?!=0` could represent the issue is reproduced. For example, if the `fuzz_target` can't run properly because of the lack of some lib, it would also return a non-0 value. We need to have a better way to check reproduction.
  - Moreover, `$?==0` doesn't mean "the bug is fixed" or "fails to reproduce". You can search "Fail to reproduce the fix" and "Fail to reproduce the crash" in the `_CrashLOGS` to find more such issues.
- Focus on newly released issues
  - As I know, the current reproducer doesn't solve many issues related to the latest released issues, because I would like to choose the middle issues as the test sample for expanding the database. But it's worth putting more attention on the new issues, as there are several new issues every day. If oss-reproducer has great performance on newly released issues, our database could increase day by day.
- transform.py
  - It's definitely a bad solution. There is some repo change its repo address. The biggest bad guy, llvm, changes to use `git` rather than `svn`. This expensive change costs me at least 100 hours. I don't want to deal with it so I use the latest oss_contain. If you have a better idea of this issue, it could improve oss-reproduce super much!
- TBD
  - I am sure there are many more tricky problems with this project. If I have time to continue writing the to-do part, I may list >20 issues... 
# Database build based on CVE-Fixes
1. Samples CWE XML file (Fast to get the samples)
2. CVE Fixes: https://github.com/n132/CVEfixes (Grab fixes for Simple Fixes take about 1-2 Hours)

[1]: https://github.com/google/oss-fuzz/tree/master/projects
