# Issue Tracer, 
# Locate the patch, based on poc and diff file
# import subprocess
from utils import *
from reproducer import *
import json
from pathlib import Path
from unidiff import PatchSet
from utils_git import * 
from base58 import b58encode

def check_build(commit,localId,pname):
    print("\n\n")
    print("*"*0x20)
    print(f"commit: {commit}")
    print("*"*0x20)
    print("\n\n")
    def leave(result):
        if CLEAN_TMP:
            clean_dir(case_dir)
        if(RM_IMAGES):
            remove_oss_fuzz_img(localId)
        return result
    srcmap,issue = getIssueTuple(localId)
    if not srcmap or not issue:
        eventLog("[-] check_build: Failed to get srcmap/issue of {localId}")
    case_dir = tmpDir()
    # Download the reproducer test case
    try:
        case_path = download_reproducer(issue,case_dir,"crash_case")
    except:
        return leave(None)
    if not case_path or not case_path.exists():
        return leave(None)
    # init srcmap
    wd = tmpDir()
    tmp_srcmap = wd / srcmap[0].name

    if(len(srcmap)==2):
        check_call(['cp',srcmap[0],tmp_srcmap])
        with open(tmp_srcmap) as f:
            data = json.load(f)
        item = "/src/"+pname
        if item in data.keys():
            data[item]['rev']=commit
        else:
            panic(f"Can't find the {item} in json data")
        with open(tmp_srcmap,'w') as f:
            f.write(json.dumps(data))
        # Test
        build_res = build_from_srcmap(tmp_srcmap,issue)
        if build_res !=True:
            return leave(None)
        res = crashVerify(issue,case_path)
        return leave(res)
    else:
        print(f"Have more than 2 Scrmap")
        return leave(None)
def dichotomy_search(commits_list,localId,pname):
    # The first commit is not tested
    # the last commit is fixed!
    print(commits_list)
    list_len = len(commits_list)
    
    if(list_len == 1):
        return commits_list[-1]
    mid = int(list_len//2)-1
    
    res = check_build(commits_list[mid],localId,pname)
    if res == None:
        return False
    elif res == True: # Not Crash
        return dichotomy_search(commits_list[:mid+1],localId,pname)
    elif res == False:# Crash
        return dichotomy_search(commits_list[mid+1:],localId,pname)
    else:
        panic(f"dichotomy_search: res->{res}")
def _cC(localId):
    # Commits Counter
    srcmap,issue = getIssueTuple(localId)
    if(len(srcmap)!=2):
        print("[-] Can't find enough srcmaps")
        return False
    pname = issue['project']
    res = list_commits(localId,pname)
    return len(res)
def gapCounter():
    issues = GetLocalIdsBetween(0,0x1000)
    res = [0]*0x1000
    for x in issues:
        tmp = _cC(x)
        if tmp!=False:
            res[tmp]+=1
    return res
def get_projectInfo(localId,pname):
    srcmap = getSrcmaps(localId)
    if(len(srcmap)!=2):
        eventLog(f"[-] list_commits: Can't find enough srcmaps: {localId}")
        exit(1)
    with open(srcmap[0]) as f:
        info1 = json.load(f)["/src/"+pname]
    with open(srcmap[1]) as f:
        info2 = json.load(f)["/src/"+pname]
    if(info1['type']!='git' or info2['type']!='git'):
        eventLog(f"[-] list_commits: Doesn't support svn & gh: {localId}")
        exit(1)
    info1['url'],info1['type'] = transform.trans_table("/src/"+pname,info1['url'],info1['type'])
    info2['url'],info2['type'] = transform.trans_table("/src/"+pname,info2['url'],info2['type'])
    return info1,info2
def list_commits(localId,pname):
    info1, info2 = get_projectInfo(localId,pname)
    print(info1['url'])
    return GitTool(OSS_DB / b58encode(info1['url']).decode() / pname ).listCommits(info1['rev'],info2['rev'])
def diff_info_parser(path):
    # return a list of modification
    # each modification would be like (file_name,start,len) 
    patch = PatchSet.from_filename(path, encoding='utf-8')
    res = [] 
    for _ in range(len(patch)):
        target_set = patch[_]
        if target_set.is_modified_file:
            file_name = target_set.source_file[1:]
            for mod in target_set:
                tmp = (file_name,mod.source_start,mod.source_length)
                res.append(tmp)
    return res
def prepare_vul_repo(commit,localId):
    issue = getIssue(localId)
    pname = issue['project']
    code_dir = OSS_DB / pname
    wk_dir = tmpDir(dont_mk=True)
    shutil.copytree(code_dir, wk_dir,symlinks=True)
    check_call(['git','reset','--hard',commit],wk_dir)
    return wk_dir
def vulCommit(localId,pname):
    
    commits = list_commits(localId,pname)
    
    if len(commits)<=1:
        return False
    commits = commits[1:]
    target_commit = dichotomy_search(commits,localId,pname)
    if target_commit == False:
        return False
    fix_idx = commits.index(target_commit)
    
    return commits[fix_idx]#,mfs

def report(localId):
    srcmap,issue = getIssueTuple(localId)
    if not verify(localId):
        eventLog(f"[-] Failed to build {localId}")
        return False
    
    if(len(srcmap)!=2):
        eventLog(f"[-] Can't find enough srcmaps for issue {localId}")
        return False
    
    pname = issue['project']
    
    with open(srcmap[0]) as f:
        info1 = json.load(f)
    
    except_name = "/src/"+pname

    if except_name in info1:
        info1 = info1[except_name]   
    else:
        with open(srcmap[1]) as f:
            info2 = json.load(f)
        first_common_key = None
        for _ in info1.keys():
            if _ in info2.keys():
                first_common_key = _
                break
        # chose the first one if it doesn't work just give up it
        if first_common_key == None:
            return False
        info1 = info1[first_common_key]
        pname = first_common_key.split("/")[-1]
        except_name = first_common_key
    
    info1['url'],_ = transform.trans_table(except_name,info1['url'],info1['type'])
    repo = info1['url']
    fix_commit= vulCommit(localId,pname)
    if fix_commit == False:
        eventLog(f"[-] Failed to locate the fixes for issue {localId}")
        return False

    #               Dump the report
    #######################################################
    if repo.startswith("https://github.com"):
        if  repo.endswith(".git"):
            repo = repo[:-4]
        repo += "/commit/"
    elif ".googlesource.com" in repo:
        repo += "/+/"
    elif repo.startswith("https://gitlab.com/") and \
        repo.endswith(".git"):
        repo = repo[:-4]+"/-/commit/"
    fix = repo+fix_commit
    
    res = dict()
    
    res['fix']      = fix
    res['verify']   = "0"
    res['localId']  = localId
    res['project']  = pname
    # data from original issues
    tmp = issue['job_type'].split("_")
    res['fuzzer']       = tmp[0]
    res['sanitizer']    = tmp[1]
    res['crash_type']   = issue['crash_type']
    try:
        res['severity'] = issue['severity']
    except:
        pass
    res['report'] = json.loads(open(DATADIR / "Issues" / (str(localId) + "_files")/(str(localId)+".json")).read())
    res['fix_commit'] = fix_commit
    res['repo_addr'] = info1['url']
    fname = oss_reproducer_dir/"Reports"/(str(localId)+".json")

    with open(fname,'w') as f:
        f.write(json.dumps(res, indent=4))
    #######################################################
    print("[+] Report Created: "+str(localId))
    return True
if __name__ == '__main__':
    report(6418)
