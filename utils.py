import re
from datetime import datetime

import subprocess
import os
import shutil
import json
import requests
import sys
import _profile
import pytz
import math
from utils import *
from pathlib import Path
from base58 import b58encode
import FailPool
from utils_exec import *
from utils_docker import *
from DB_Manager import *
import inspect
#==================================================================
#
#                          Global Settings
#
#==================================================================
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = _profile.gcloud_key
oss_fuzz_dir = Path(_profile.oss_fuzz_dir)
oss_reproducer_dir = _profile.oss_reproducer_dir
OSS_OUT     = Path(_profile.OSS_OUT_DIR)
OSS_WORK    = Path(_profile.OSS_WORK_DIR)
OSS_TMP     = Path(_profile.TMP)

RM_IMAGES = True
CLEAN_TMP = _profile.CLEAN_TMP 
FORCE_CLEAN = False
TIME_ZONE =  _profile.TIME_ZONE
DATADIR = Path(oss_reproducer_dir) / _profile.DATA_FOLD
MetaDataFile = DATADIR / "metadata.jsonl"
session = requests.Session()

def eventLog(s):
    with open(Path(oss_reproducer_dir)/"Log"/"_Event.log",'a') as f:
        f.write(s+"\n")
sys.path.insert(1,str(oss_fuzz_dir/"infra"))
def dir_check(path):
    try:
        if not path.exists():
            path.mkdir()
        return True
    except:
        return False
def file_check(path):
    try:
        if not path.exists():
            path.touch()
        return True
    except:
        return False
def json_file_check(path):
    try:
        if not path.exists():
            path.touch()
            with open(path,'w') as f:
                f.write(json.dumps(dict(),indent=4))
        return True
    except:
        return False
def panic(s):
    print(s)
    exit(1)

# Init Dirs
if not dir_check(OSS_TMP) or not dir_check(OSS_OUT) or not dir_check(OSS_WORK) or not dir_check(OSS_DB):
    panic("Failed to init OSS_OUT/OSS_WORK/OSS_DB")
if not OSS_DB_MAP.exists():
    OSS_DB_MAP.touch()
    with open(OSS_DB_MAP,'w') as f:
        f.write(json.dumps(dict(),indent=4))
#==================================================================
#
#                          Global Settings END
#
#==================================================================
def getPname(localId):
    srcmap,issue = getIssueTuple(localId)
    pname = issue['project']
    with open(srcmap[0]) as f:
        info1 = json.load(f)
        except_name = "/src/"+pname
        if except_name in info1:
            info1 = info1[except_name]   
        else:
            first_item = list(info1.keys())[0]
            info1 = info1[first_item]
            # Chose the first one 
            # If it doesn't work
            # the caller would decide 
            # if we should give up this case
            pname = first_item.split("/")[-1]
    return pname
def find_issues_by_names(pro_names):
    res = []
    with open(MetaDataFile) as f:
        while(1):
            line = f.readline()
            if(not line):
                break
            line = json.loads(line)
            try:
                pro = line["project"]
                if(pro in pro_names):
                    if line['localId'] not in FailPool.noreg:
                        res.append(line['localId'])
            except:
                pass
    return res
def get_project_by_localids(localIds):
    res = []
    dt = dict()
    with open(MetaDataFile) as f:
        while(1):
            line = f.readline()
            if(not line):
                break
            line = json.loads(line)
            dt[line['localId']] = line
    for _ in localIds:
        try:
            res.append(dt[_]['project'])
        except:
            res.append("UNK")
    return res

def GetLocalIdsBetween(start,end):
    res = []
    with open(MetaDataFile) as f:
        while(1):
            line = f.readline()
            if(not line):
                break
            line = json.loads(line)
            localId = int(line['localId'])
            if localId>= start and localId <= end:
                res.append(localId)
    return res
def GetAllLocalIds():
    return GetLocalIdsBetween(0,math.inf)
def getIssueTuple(localId):
    srcmap = getSrcmaps(localId)
    issue  = getIssue(localId)
    return srcmap,issue
def getSrcmaps(localId):
    def _cmp(a):
        return str(a)
    issue_dir = DATADIR / "Issues" / (str(localId) + "_files")
    if not issue_dir.exists():
        eventLog(f"[-] no such issue_dir for {localId}")
        return False
    srcmap = list(issue_dir.glob('*.srcmap.json'))
    srcmap.sort(key=_cmp)
    return srcmap
def getIssue(localId):
    data = get_metadata()
    for _ in data:
        issue = json.loads(_)
        if(issue['localId']==localId):
            return issue
    eventLog(f"[-] no such issue, {localId}")
    return False
def tmpDir(path=OSS_TMP,pre="n132_",dont_mk=False):
    name = pre+b58encode(os.urandom(16)).decode()
    res = Path(path)
    res = res/name
    if(not dont_mk):
        res.mkdir()
    return res
def tmpFileName(n=0x10):
    return b58encode(os.urandom(n)).decode()
def tmpFile():
    tmpfile = tmpDir() / tmpFileName()
    tmpfile.touch()
    return tmpfile
#======================================
#          clone/checkout START
#======================================
def repo_exist(url,dest,name):
    records = DB_MAP()
    if url in records.keys():
        original_dir = records[url]
        if Path(original_dir).exists():
            if name == None:
                name = Path(original_dir).name
            try:
                shutil.copytree(original_dir,dest/name,symlinks=True)
                return True
            except:
                return False
        else:
            DB_remove(url,Path(original_dir))
            return False
    else:
        return False 
def _git_clone(url,dest,name):
    if dest == OSS_DB:
        eventLog(f"[!] Forbiden: Naming the repo in OSS_DB")
        exit(1)
    if repo_exist(url,dest,name):
        return True
    # We have to clone it
    cmd = ['git','clone',url]
    if name != None:
        cmd.append(name)
    if not check_call(cmd,dest):
        return False
    if name == None:
        name = list(dest.iterdir())[0]
    # Insert it to the database
    return DB_INSERT(url,dest/name)

def _hg_clone(url,dest=None,name=None):
    cmd = "hg clone".split(" ")
    cmd +=[url]
    if name:
        cmd.append(name)
    if dest:
        return execute(cmd,dest)
    return execute(cmd)
def _svn_clone(url,dest=None,name=None):
    cmd = "svn co".split(" ")
    cmd +=[url]
    if name:
        cmd.append(name)
    if dest:
        return execute(cmd,dest)
    return execute(cmd)
def _check_out(commit,path):
    return check_call(['git',"reset",'--hard', commit], cwd=path)
def _hg_check_out(commit,path):
    return check_call(['hg',"checkout", commit], cwd=path)
def _svn_check_out(commit,path):
    return check_call(['svn',"up",'-r', commit], cwd=path)
def clone(url,commit=None,dest=None,name=None):
    if(dest):
        dest = Path(dest)
    else:
        dest = tmpDir()
    
    if not _git_clone(url,dest,name):
        eventLog(f"[!] - clone: Failed to clone {url}")
        return False
    
    if commit:
        print(f"[+] Checkout to commit {commit}")
        if name==None:
            name = list(dest.iterdir())[0]
        if _check_out(commit,dest / name):
            return dest
        else:
            eventLog(f"[!] - clone: Failed to checkout {name}")
            return False
    return dest
def hg_clone(url,commit=None,dest=None,rename=None):
    try:
        if(dest):
            tmp = Path(dest)
        else:
            tmp = tmpDir()
        _hg_clone(url,tmp,rename)
        if commit:
            if rename:
                name = rename
            else:
                if url.split("/")[-1]!="":
                    name = url.split("/")[-1]
                else:
                    name = url.split("/")[-2]
            #ugly code but I don't want to fix it
            tmp = tmp / name
            _hg_check_out(commit,tmp)
    except:
        return False
    return tmp
def svn_clone(url,commit=None,dest=None,rename=None):
    try:
        if(dest):
            tmp = Path(dest)
        else:
            tmp = tmpDir()
        _svn_clone(url,tmp,rename)
        if commit:
            if rename:
                name = rename
            else:
                if url.split("/")[-1]!="":
                    name = url.split("/")[-1]
                else:
                    name = url.split("/")[-2]
            #ugly code but I don't want to fix it
            tmp = tmp / name
            _svn_check_out(commit,tmp)
    except:
        return False
    return tmp
#======================================
#          clone/checkout END
#======================================
def clean_dir(victim):
    if victim.exists():
        try:
            shutil.rmtree(victim)
            return True
        except:
            return False
def remove_oss_fuzz_img(localId):
    try:
        print(f"[+] Delete images, {localId}")
        print("*"*0x20)
        imgName = f"gcr.io/oss-fuzz/{localId}"
        cmd = "docker images -q".split()
        imageHash = execute(cmd+[imgName])
        imageHash = imageHash.decode().strip().replace("\n","")
        cmd = f"docker image rm {imgName}".split(" ")
        print(" ".join(cmd))
        execute(cmd)
        cmd = ("docker image rm "+imageHash).split(" ")
        print(" ".join(cmd))
        execute(cmd)
        print("*"*0x20)
    except:
        panic("[!] Fail to remove Changed Images")
def crash_verfiy(issue,reproduce_case,bt=False,local=True):
    print(" "*0x20)
    print("$"*0x20)
    print(" "*0x20)
    build_out = OSS_OUT
    # project_name = issue['project']
    # Find the fuzzer target
    if "fuzz_target" in issue.keys():
        fuzz_target = build_out / str(issue['localId']) / issue['fuzz_target']
    elif "fuzzer" in issue.keys():
        fuzz_target = build_out / str(issue['localId']) / issue['fuzzer']
    else:
        try:
            fuzz_target = build_out / str(issue['localId']) / issue['issue']['summary'].split(":")[1]
        except:
            issue_record(issue['project'],issue['localId'],f"Doesn't specify a fuzzer")
            return None
    try:
        file_exist = fuzz_target.exists()
    except:
        cmd = ['docker','run','--rm','--privileged']
        localId=issue['localId']
        args = ['-v',f'{fuzz_target.parent.parent}:/mnt','-t','ubuntu','chmod','777',f'/mnt/{localId}']
        cmd.extend(args)
        # print(" ".join(cmd))
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
        __,_ = p.communicate()
        file_exist = fuzz_target.exists()
    if not file_exist:
        issue_record(issue['project'],issue['localId'],f"Fuzz target {str(fuzz_target)} doesn't exist")
        return None
    res = ifcrash(str(fuzz_target),str(reproduce_case),bt,local)
    print(" "*0x20)
    print("$"*0x20)
    print(" "*0x20)
    return res
def ifcrash(fuzz_target,case,bt=False,local=True):
    name = fuzz_target.split("/")[-1]
    input_name = case.split("/")[-1]
    tmp_dir = tmpDir()
    binary = tmp_dir/name
    shutil.copyfile(fuzz_target, binary)
    shutil.copyfile(case, tmp_dir/input_name)
    if check_call(["chmod","+x",str(binary)]):
        if local:
            try:
                res = _ifcrash_local([str(binary),str(tmp_dir/input_name)],bt)
            except:
                res = _ifcrash(['-v',f"{tmp_dir}:/tmp","ubuntu",'/tmp/'+name,'/tmp/'+input_name],case,bt)
        else:
            res = _ifcrash(['-e','ASAN_OPTIONS=detect_leaks=0','-v',f"{tmp_dir}:/tmp","ubuntu",'/tmp/'+name,'/tmp/'+input_name],case,bt)
        if CLEAN_TMP:
            shutil.rmtree(tmp_dir)
        return res
    else:
        print(f"[!] Failed on `chmod +x {binary}`")
        if CLEAN_TMP:
            shutil.rmtree(tmp_dir)
        return False

def _ifcrash_local(cmd,bt=False):
    print(" ".join(cmd))
    cwd = Path(OSS_TMP)
    IGN_MEMLEAK={'ASAN_OPTIONS':"detect_leaks=0"}
    p = subprocess.Popen(cmd,stderr=subprocess.STDOUT,cwd=cwd,env=IGN_MEMLEAK)
    __,_ = p.communicate()
    if p.returncode == -6:
        p = subprocess.Popen(cmd[0],stdin=open(cmd[1]),
                            stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                            cwd=cwd,env=IGN_MEMLEAK)
        __,_ = p.communicate()
    if(p.returncode == 0):
            return True
    else:
        if bt == False:
            return False
        else:
            p = subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 cwd=cwd,env=IGN_MEMLEAK)
            __,_ = p.communicate()
            return asan_parser(__)
def _ifcrash(args,case,bt=False):
    cmd = ['docker','run','--rm','--privileged']
    cmd.extend(args)
    print(" ".join(cmd))
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
    __,_ = p.communicate()
    if p.returncode == -6:
        p = subprocess.Popen(cmd[:-1],stdin=open(case),stdout=subprocess.PIPE)
        __,_ = p.communicate()
    if(p.returncode == 0):
            return True
    else:
        if bt == False:
            return False
        else:
            p = subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            __,_ = p.communicate()
            return asan_parser(__)

def asan_parser(res):
    lines = res.split(b"\n")
    bt_mark = b'    #0'
    bt = [] 
    for x in range(len(lines)):
        if(lines[x][:len(bt_mark)]==bt_mark):
            for y in range(3):
                bt.append(lines[x+y].split()[3])
            print(bt)
            return bt
def download_reproducer(issue,path,name):
    global session
    session = requests.Session()
    url = issue['reproducer']
    response = session.head(url, allow_redirects=True)
    
    if response.status_code != 200:
        return False
    reproducer_path = path / name
    response = session.get(url)
    
    if response.status_code != 200:
        return False
    reproducer_path.write_bytes(response.content)
    return reproducer_path
def getSanitizer(fuzzer_sanitizer):
    if(fuzzer_sanitizer=='asan'):
        fuzzer_sanitizer    ="address"
    elif(fuzzer_sanitizer=='msan'):
        fuzzer_sanitizer    ='memory'
    elif(fuzzer_sanitizer=='ubsan'):
        fuzzer_sanitizer    ='undefined'
    else:
        fuzzer_sanitizer = False
    return fuzzer_sanitizer
def get_metadata():
    with open(MetaDataFile) as f:
        data = f.readlines()
    return data
def _list_with_time(date,repo="gcr.io/oss-fuzz-base/base-builder"):
    cmd =f"gcloud container images list-tags {repo}"
    cmd+=f''' --format="table(digest.slice(7:).join(''))"'''
    cmd+=f' --filter="timestamp.datetime <= {date} "'
    cmd+=f' --limit 1'
    print(f"[+] Running:\n{cmd}\n")
    try:
        res = os.popen(cmd).read() 
        match = re.search(r"[a-f0-9]{64}",res)
        return match.group(0)
    except:
        return False

def rebaseDockerfile(dockerfile_path,commit_date):
    try:
        with open(dockerfile_path) as f:
            data = f.read()
    except:
        eventLog(f"[-] rebaseDockerfile: No such a dockerfile: {dockerfile_path}")
        return False
    res = re.search(r'FROM .*',data)
    if(res == None):
        eventLog(f"[-] rebaseDockerfile: Failed to get the base-image: {dockerfile_path}")
        return False
    image_hash = _list_with_time(commit_date)
    if not image_hash :
        # Use the latest image
        eventLog(f"[-] rebaseDockerfile: Failed to find a valid base-builder, use the latest version...")
        data = re.sub(r"FROM .*",f"FROM gcr.io/oss-fuzz-base/base-builder",data)
        with open(dockerfile_path,'w') as f:
            f.write(data)
        return True
    image_name = "gcr.io/oss-fuzz-base/base-builder"
    data = re.sub(r"FROM .*",f"FROM {image_name}@sha256:"+image_hash+"\nRUN apt-get update -y\n",data)
    with open(dockerfile_path,'w') as f:
        f.write(data)
    return True
def fixDockerfile(dockerfile_path,project=None):
    # todo: if you want to make it faster, implement it. And it's a liitle complex
    # DO not want to modify dockerfile
    # It comsumes TIME! 
    dft = DfTool(dockerfile_path)
    if project in ["php","harfbuzz"]:
        assert(dft.replace(r'RUN git .*',"")==True)
        assert(dft.replace(r'COPY .*\$SRC.*',"")==True)
    elif project == 'poppler':
        assert(dft.replace(r"RUN apt update.*",'RUN git config --global http.sslVerify false')==True)
        assert(dft.replace(r'COPY .*\$SRC.*',"")==True)
    elif project == 'libreoffice':
        assert(dft.replace(r'ADD .*',"")==True)
        assert(dft.replace(r'RUN cd afl-testcases.*',"")==True)
        assert(dft.replace(r'RUN zip.*',"")==True)
    elif project == 'imagemagick':
        assert(dft.replace("ADD http://lcamtuf","ADD https://lcamtuf")==True)
        assert(dft.replace(r'RUN git .*freetype2.*',"")==True)
    elif project == "libxml2":
        assert(dft.replace(r"RUN git clone .*libxml2.*","")==True)
    elif project =="dav1d":
        assert(dft.replace(r'RUN git clone .*dav1d.*',"")==True)
    elif project == "yara":
        if 'bison' not in dft.content:
            line = "RUN git clone --depth 1 https://github.com/VirusTotal/yara.git"
            assert(dft.insertLineBefore(line,"RUN apt install -y bison")==True)
    elif project == "gdal":
        pass
        # line = "RUN apt update -y"
        # assert(dft.insertLineAfrer(line,"RUN apt install -y curl")==True)
    elif project == "lwan":
        assert(dft.replace(r"RUN git.*lwan.*","")==True)
    elif project == "radare2":
        assert(dft.replace(r"RUN git clone .*radare2.*","")==True)
        assert(dft.replace(r"RUN git clone .*regressions.*","")==True)
    elif project == "wireshark":
        assert(dft.replace(r"RUN git clone .*wireshark.*","")==True)
    print("[+] Dockerfile: Fixed")
    return True
def extraScritps(pname,oss_dir,source_dir):
    # This function is redundant after fix the timestap issue
    # if pname == "gdal":
    #     target1 = source_dir/"src"/"gdal"/"gdal"/"fuzzers"/"build.sh"
    #     target2 = source_dir/"src"/"gdal"/"fuzzers"/"build.sh"
    #     if target1.exists():
    #         shutil.copyfile(target1,oss_dir/"build.sh")
    #     elif target2.exists():
    #         shutil.copyfile(target2,oss_dir/"build.sh")
    #     else:
    #         return False
    
    return True
def stamp2date(out):
    tz = pytz.timezone(TIME_ZONE)
    out = int(out)
    res = datetime.fromtimestamp(out, tz)#.isoformat()
    return res     
def str2date(issue_date):
    return datetime.strptime(issue_date+" +0000", '%Y%m%d%H%M %z')
def git_date(commit,path):
    # print(commit,path)
    cmd = ["git","show","-s","--format=%ct",commit]
    out = execute(cmd,path)
    if out == b"":
        return False
    return stamp2date(out)
def svn_date(commit,path):
    #todo
    return None
def hg_date(commit,path):
    #todo
    return None
def issue_record(name,localId,des,log_addr = "_CrashLOGs"):
    filename = Path(oss_reproducer_dir) / log_addr
    with open(filename,'a+') as f:
        f.write(f"| {name} | {localId} | {des} |\n")
    return 
def result_record(project,localId,result):
    filename = Path(oss_reproducer_dir) / "Results.json"
    payload = {}
    payload['localId'] = localId
    payload['project'] = project
    payload['pass'] = result
    with open(filename,'a+') as f:
        f.write(json.dumps(payload)+'\n')
    return 
def project_language(project):
    tmp = oss_fuzz_dir / "projects" / project
    res = list(tmp.glob("project.yaml"))
    if(len(res)!=1):
        eventLog(f"[-] project_language: Fail to locate {project}'s project.ymal")
        return "c++"
    else:
        with open(res[0]) as f:
            data = f.read()
        res = re.findall(r'language\s*:\s*([^\s]+)',data)
        if len(res) > 1:
            return str(res[0])
        else:
            return "c++"
def fixBuildScript(file,pname):
    if not file.exists():
        return True
    dft = DfTool(file)
    if pname=="uwebsockets":
        '''
        https://github.com/alexhultman/zlib
        ->
        https://github.com/madler/zlib.git
        '''
        script = "sed -i 's/alexhultman/madler/g' fuzzing/Makefile"
        assert(dft.insertLineat(0,script)==True)
    return True

def additional_script(project,source_path=None):
    if project =="poppler":
        tmp = source_path/"poppler"/'fuzz'
        tmp.mkdir()
        for x in list(source_path.glob('*.cc')):
            cmd=['cp',str(x),str(tmp)]
            execute(cmd,cwd=source_path)
    return True    

def remove_issue_meta(localIds):
    data = get_metadata()
    data  = [json.loads(x) for x in data]
    new_data = []
    for x in data:
        if x['issue']['localId'] not in localIds:
            new_data.append(x)
    with open(MetaDataFile,'w') as f:
        for x in new_data:
            f.write(json.dumps(x)+'\n')
def remove_issue_data(localIds):
    target = DATADIR/"Issues"
    for x in localIds:
        fname = str(x)+"_files"
        try:       
            shutil.rmtree(target/fname)
        except:
            pass
def issue_filter():
    localids = GetAllLocalIds()
    res = []
    for localId in localids:
        target_dir = Path(DATADIR)/"Issues"/(str(localId)+"_files")
        if len(list(target_dir.iterdir())) <3:
            res.append(localId)
            print(f"[!] Have less than 2 srcmaps, deleting issue {localId}...")
    remove_issue_meta(res)
    remove_issue_data(res)
    print("Done")

if __name__ == "__main__":
    pass