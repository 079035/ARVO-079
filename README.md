# ARVO

ARVO: an Atlas of Reproducible Vulnerabilities in
Open source software. By sourcing vulnerabilities from C/C++
projects discovered by Google’s OSS-Fuzz, we are able to
automatically build a benchmark for vulnerability repair with
more near 3,000 vulnerabilities across 231 projects, each with
a triggering input and the canonical developer-written patch
for fixing the vulnerability. Moreover, our dataset can be
automatically updated as OSS-Fuzz finds new vulnerabilities,
mitigating issues of training data contamination and overfit-
ting. 

# Reports

For ease of access and organization, all reports related to ARVO can be found in [this][2] directory. 


# Compiled Database

Open Website: anonymized...

To maximize user convenience and efficiency, ARVO provides pre-compiled cases, each compressed into a Docker image that can be easily downloaded from the Internet. This approach ensures that users can access and utilize these cases with minimal effort and technical overhead.

The process of accessing and using these Docker images is designed to be straightforward, involving just three simple commands:

```
wget <url>
docker load < *-Vul.tar
source *_vul.sh
```

Additionally, the same command sequence can be applied to the fixed versions of these cases. This allows users to not only reproduce vulnerabilities but also verify the effectiveness of the fixes applied.

# Build the Database

- Run ARVO on Linux/Unix OS
- Install gcloud and required python modules
- Clone ARVO from Github
- Create and config `_profile.py`, there is an example for your [referrence][3]
- Create the directory for ARVO
- We are ready to use ARVO

# Warning

You need to finish previous section first. Then use CLI and Benchmark.

# CLI Interface

```
[+] Usage:
[+]      python3 cli.py [Command] [LocalId]
[+]      Command: <reproduce, report>
[+]      LocalId: a number identifier for the issue in OSS-Fuzz
```

# Benchmark Interface


You can also use the API function `cli_getMeta` and `cli_tryFIx`, or the script to interacte with ARVO.
For `tryFix`, we now only support one-function related fix.

## getMeta

```py
python3 ./BenchmarkCLI.py getMeta <localId>
```

## tryFix

```py
python3 ./BenchmarkCLI.py getMeta <localId> <FixFile>
```



[1]: https://github.com/google/oss-fuzz/tree/master/projects
[2]: ./Reports
[3]: ./Setting.md
