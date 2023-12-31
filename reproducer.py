from utils import *
from glob import glob
sys.path.insert(1,oss_fuzz_dir/"infra")
import build_specified_commit as builder
import transform

# Global
DEAMON_CMD = []


def parse_copy(src,dst,project_dir,wkdir = None):
    print(f"[+] Dockerfile COPY: {src} -> {dst}")
    # Parse dst
    if dst.startswith("$SRC"):
        dst = Path(dst.replace("$SRC","/src"))
    elif dst.startswith("/"):
        dst = Path(dst)
    else:
        #relative path
        if wkdir!=None:
            dst = Path("/src") / wkdir / dst                      
        else:
            dst = Path("/") / dst
    # parsing source files
    src_files = glob(str(project_dir)+'/'+src)
    targets = []
    for src_file in src_files:
        if dst.name != src_file.split('/')[-1]:
            targets += [str(src_file), str(dst/src_file.split('/')[-1])]
        else:
            targets += [str(src_file), str(dst)]
    return targets
def combineLines(lines):
    res = []
    flag = 0
    for line in lines:
        if flag==1:
            if not line.endswith("\\\n"):
                buf+= line
                res.append(buf)
                flag=0
            else:
                buf+=line[:-1]
        else:
            if not line.endswith("\\\n"):
                res.append(line) 
            else:
                buf = line[:-1]
                flag=1
    return res
def parse_dockerfile(project_dir):
    # pname = project_dir.name
    config_file = Path(project_dir)/"Dockerfile"
    with open(config_file,"r") as f:
        lines = f.readlines()
    wkdir = None
    targets = []

    lines = combineLines(lines)

    for line in lines:
        if line.startswith("#"):
            continue
        elif "WORKDIR" in line:
            wkdir = line.split()[-1]
        elif "COPY" in line:
            # taking care of desination
            res=line.split()[1:] # COPY SRC DEST
            if len(res)!=2:
                for src in res[:-1]:
                    targets+= parse_copy(src,res[-1],project_dir,wkdir)
            else:
                targets+= parse_copy(res[0],res[1],project_dir,wkdir)
        else:
            pass
        # Other Dockerfile COMMANDs
    if targets == []:
        # print("No Copy Command Found")
        # Copy everything
        for config_file in project_dir.iterdir():
            name = config_file.name
            if name == "Dockerfile" or name =="project.yaml":
                continue
            elif name == "build.sh":
                targets+= [str(config_file),"/src/build.sh"]
            else:
                targets+= [str(config_file),str(Path("/src")/name)]
    return targets
def leaveRet(res,tmpdir):
    if CLEAN_TMP:
        if type(tmpdir) !=type([]):
            clean_dir(tmpdir)
        else:
            for _ in tmpdir:
                clean_dir(_)
    return res

def build_from_srcmap(srcmap,issue,replace_dep=None,save_img=False):
    # Get Sanitizer
    fuzzer_info = issue['job_type'].split("_")
    engine = fuzzer_info[0]
    sanitizer = getSanitizer(fuzzer_info[1])
    if sanitizer == False:
        return False
    # Get Arch
    if fuzzer_info[2] == 'i386':
        arch='i386'
    else:
        arch='x86_64'
    return build_fuzzer_with_source(issue['issue']['localId'],issue['project'],\
            srcmap,sanitizer,engine,arch,replace_dep=replace_dep,\
            save_img=save_img)
    
def prepareOSSFuzz(project_name,commit_date):
    # 1. Clone OSS Fuzz
    tmp_dir          = clone("https://github.com/google/oss-fuzz.git",name="oss-fuzz")
    # 2. Get the Commit Close to Commit_Date
    tmp_oss_fuzz_dir = tmp_dir / "oss-fuzz"
    cmd = ['git','log','--before='+ commit_date.isoformat(), '-n1', '--format=%H']
    oss_fuzz_commit = execute(cmd,tmp_oss_fuzz_dir).strip()
    if not oss_fuzz_commit:
        cmd = ['git','log','--reverse', '--format=%H']
        oss_fuzz_commit = execute(cmd,tmp_oss_fuzz_dir).splitlines()[0].strip()
        if not oss_fuzz_commit:
            eventLog('[-] prepareOSSFuzz: Failed to get oldest oss-fuzz commit')
            return leaveRet(False,tmp_dir)
    # 3. Reset OSS Fuzz
    try:
        cmd = ['git','reset','--hard',oss_fuzz_commit]
        execute(cmd,tmp_oss_fuzz_dir)
    except:
        eventLog("[-] prepareOSSFuzz: Fail to Reset OSS-Fuzz")
        return leaveRet(False,tmp_dir)
    # 4. Locate Project Dir
    tmp_list = [x for x in tmp_oss_fuzz_dir.iterdir() if x.is_dir()]
    if tmp_oss_fuzz_dir/ "projects" in tmp_list:
        proj_dir = tmp_oss_fuzz_dir/ "projects" / project_name
    elif tmp_oss_fuzz_dir/ "targets" in tmp_list:
        proj_dir = tmp_oss_fuzz_dir/ "targets" / project_name
    else:
        eventLog("[-] prepareOSSFuzz: Fail to locate the project")
        return leaveRet(False,tmp_dir)
    return (tmp_dir, proj_dir)
def build_fuzzer_with_source(localId,project_name,srcmap,sanitizer,engine,arch,replace_dep=None,\
    save_img=False):
    # Get Issue Date
    

    issue_date = srcmap.name.split(".")[0].split("-")[-1]
    commit_date = str2date(issue_date)
    
    # Reset OSS-Fuzz to get Dependencies 
    res = prepareOSSFuzz(project_name,commit_date)
    if not res:
        return res
    else:
        tmp_dir , project_dir = res
    # checkout oss  
    dockerfile = project_dir / 'Dockerfile'
    print(f"[+] dockerfile: {dockerfile}")
    build_data = builder.BuildData(
        sanitizer=sanitizer,
        architecture=arch,
        engine=engine,
        project_name=project_name)
    # Build source_dir
    def rootRM(dir_path):
        if CLEAN_TMP:
            dir_name = str(dir_path).split("/")[-1]
            docker_run(["-v", f"{OSS_TMP}:/mnt" , "ubuntu", "/bin/bash", "-c",
                        f"rm -rf /mnt/{dir_name}"])
    
    with open(srcmap) as f:
        data = json.loads(f.read())
    source_dir = tmpDir()
    src = source_dir / "src"
    src.mkdir(parents=True, exist_ok=True)
    docker_volume = []
    for x in data.keys():
        print(f"[+] Prepare Dependency: {x}")
        item_name = x
        item_url = data[x]['url']
        item_type = data[x]['type']
        item_rev = data[x]['rev']
        
        item_url,item_type = transform.trans_table(item_name,item_url,item_type)
        item_name = "/".join(item_name.split("/")[2:])
        if item_rev=="" or item_rev == "UNKNOWN":
            print(f"[-] No Rev Provided")
            shutil.rmtree(source_dir)
            return leaveRet(False,tmp_dir)
        if item_name == "":
            if(len(data.keys())==1):
                shutil.rmtree(source_dir)
                return leaveRet(False,tmp_dir)
            else:
                continue
        if(item_type=='git'):
            if(item_name == 'aflplusplus' and\
                item_url =='https://github.com/AFLplusplus/AFLplusplus.git'):
                print("[+] AFL++: Using latest fuzz-base")
                continue
            clone_res = clone(item_url,item_rev,src,item_name)
            if clone_res == False:
                eventLog(f"[!] build_from_srcmap: Failed to clone & checkout [{localId}]: {item_name}")
                shutil.rmtree(source_dir)
                return leaveRet(False,tmp_dir)
            elif clone_res == None:
                latest_date =  str(commit_date)[:10]
                command = f'git log --before="{latest_date}" -n 1 --format="%H"'
                res = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True,cwd=src/item_name)
                res = res.stdout.strip()
                if check_call(['git',"reset",'--hard', res], cwd=src/item_name) == False:
                    eventLog(f"[!] build_from_srcmap: Failed to clone & checkout [{localId}]: {item_name}")
                    shutil.rmtree(source_dir)
                    return leaveRet(False,tmp_dir)
            docker_volume.append(x)
        elif(item_type=='svn'):
            if(item_name == 'libfuzzer' and\
                item_url =='https://llvm.org/svn/llvm-project/compiler-rt/trunk/lib/fuzzer'):
                print("[+] libfuzzer, Using latest fuzz-base")
                continue
            elif not svn_clone(item_url,item_rev,src,item_name):
                eventLog(f"[!] build_from_srcmap: Failed clone & checkout: {item_name}")
                shutil.rmtree(source_dir)
                return leaveRet(False,tmp_dir)
            docker_volume.append(x)
        elif(item_type=='hg'):
            if not hg_clone(item_url,item_rev,src,item_name):
                eventLog(f"[!] build_from_srcmap: Failed clone & checkout: {item_name}")
                shutil.rmtree(source_dir)
                return leaveRet(False,tmp_dir)
            docker_volume.append(x)
        elif(item_type=='unknown'):
            eventLog(f"[!] build_from_srcmap: Broken Srcmap")
            shutil.rmtree(source_dir)
            return leaveRet(False,tmp_dir)
        else:
            shutil.rmtree(source_dir)
            leaveRet(False,tmp_dir)
            panic(f"[-] build_from_srcmap: New type found, {item_type}")
    
    if replace_dep != None and replace_dep[1].exists():
        target_addr = src/replace_dep[0]
        shutil.rmtree(target_addr)
        check_call(['cp','-r',replace_dep[1],target_addr])

    # Step ONE: Rebase Dockerfiles
    if not rebaseDockerfile(dockerfile,str(commit_date).replace(" ","-")):
        eventLog(f"[-] build_fuzzer_with_source: Fail to Rebase Dockerfile, {localId}")
        rootRM(source_dir)
        return leaveRet(False,tmp_dir)
    # Step TWO: Fix Dockerfiles 
    if not fixDockerfile(dockerfile,project_name):
        eventLog(f"[-] build_fuzzer_with_source: Fail to Fix Dockerfile, {localId}")
        rootRM(source_dir)
        return leaveRet(False,tmp_dir)
    # Step Three: Extra Scripts
    if not extraScritps(project_name,project_dir,source_dir):
        eventLog(f"[-] build_fuzzer_with_source: Fail to Run ExtraScripts, {localId}")
        rootRM(source_dir)
        return leaveRet(False,tmp_dir)    
    if not fixBuildScript(project_dir/"build.sh",project_name):
        eventLog(f"[-] build_fuzzer_with_source: Fail to Fix Build.sh, {localId}")
        rootRM(source_dir)
        return leaveRet(False,tmp_dir)
    # Let's Build It
    result = build_fuzzers_impl(localId,project=project_name,
                                project_dir= project_dir,
                                engine=build_data.engine,
                                sanitizer=build_data.sanitizer,
                                architecture=build_data.architecture,
                                source_path= source_dir/"src",
                                mount_path=Path("/src"),
                                save_img=save_img)
    rootRM(source_dir)
    return leaveRet(result,tmp_dir)
def build_fuzzers_impl( localId,project,project_dir,engine,
    sanitizer,architecture,source_path,
    mount_path=None,save_img=False):
    global DEAMON_CMD
    project_out  = OSS_OUT  / str(localId) 
    project_work = OSS_WORK / str(localId)
    
    if not project_out.exists():
        project_out.mkdir()        
    if not project_work.exists():
        project_work.mkdir()
    
    args = ['-t',f'gcr.io/oss-fuzz/{localId}','--file', str(project_dir/"Dockerfile"), str(project_dir)]
    
    if not docker_build(args):
        return False
    
    print('[+] Cleaning existing out dir')
    docker_run([
        '-v',
        '%s:/out' % project_out , '-t',
        f'gcr.io/oss-fuzz/{localId}', '/bin/bash', '-c', 'rm -rf /out/*'
    ])
    docker_run([
        '-v',
        '%s:/work' % project_work , '-t',
        f'gcr.io/oss-fuzz/{localId}', '/bin/bash', '-c', 'rm -rf /work/*'
    ])
    env = [
        'FUZZING_ENGINE=' + engine,
        'SANITIZER=' + sanitizer,
        'ARCHITECTURE=' + architecture,
        'FUZZING_LANGUAGE=' + project_language(project),
    ]
    command = sum([['-e', x] for x in env], [])

    additional_script(project,source_path)
    if source_path and mount_path:
        for item in source_path.iterdir():  
            command += [
                '-v',
                '%s:%s' % (item, mount_path / item.name),
            ]
    targets = parse_dockerfile(project_dir)
    for i in range(0,len(targets),2):
        command += [
            '-v',
            '%s:%s' % (targets[i],targets[i+1])
        ]
    command += [
            '-v',
            '%s:/out' % project_out, '-v',
            '%s:/work' % project_work, '-t',
            f'gcr.io/oss-fuzz/{localId}'
    ]

    if save_img != False:
        result = docker_run(["--name",f"arvo_deamon_{localId}_{save_img}"]+command,rm=False)
    else:
        result = docker_run(command)
    if not result:
        print('[-] Failed to Build Targets')
        return False
    
    if save_img != False:
        DEAMON_CMD = []
        cur_idx = 0 
        deamon = ["-d","--name",f"reproducer_{localId}"]
        cps = []
        while(cur_idx < len(command)):
            if command[cur_idx] == "-v":
                dirs = command[cur_idx+1].split(":")
                cps.append((dirs[0],dirs[1]))
                cur_idx +=2
            elif command[cur_idx] == "-t":
                deamon.append("-t")
                deamon.append(command[cur_idx+1])
                deamon.append("sleep")
                deamon.append("infinity")
                cur_idx +=2
            elif command[cur_idx] == "-e":
                DEAMON_CMD.append("-e")
                DEAMON_CMD.append(command[cur_idx+1])
                cur_idx +=2
            else:
                deamon.append(command[cur_idx])
                cur_idx +=1
        # Spawn a deamon container
        
        docker_run(deamon,rm=False)
        # Copy the mounted file to the deamon container
        assert("-v" not in deamon)
        for pr in cps:
            # find /opt/lampp/htdocs -type d -exec chmod 755 {} \;
            permissionResolve(pr[0])
            if Path(pr[0]).is_dir():
                docker_exec(f"reproducer_{localId}",["rm","-rf",pr[1]])
            assert(docker_cp(pr[0],f"reproducer_{localId}:"+pr[1])==True)
        # Save the command which includes ENV
    return True
def permissionResolve(target_path):
    # Test Code to make testing faster
    res = execute_ret(["sudo","chown","-R",f"{UserName}:{UserName}",target_path])
    print(f"[+] Chown result = {res}")
    #docker_run(["-v",f"{target_path}:/tmp/target","ubuntu", "/bin/bash", "-c","find /tmp/target -type d -exec chmod +rw {} +"])
    #docker_run(["-v",f"{target_path}:/tmp/target","ubuntu", "/bin/bash", "-c","find /tmp/target -type f -exec chmod +r {} +"])

def saveCommand(fpath,image,issue):
    fuzz_target = getFuzzTarget(issue).name
    tmp = ["docker","run","--rm","--privileged"] + ['-e','ASAN_OPTIONS=detect_leaks=0']
    tmp += DEAMON_CMD
    tmp += ["-t",image,f"/out/{fuzz_target}","/tmp/poc"]
    # print(" ".join(tmp)+"\n")
    with open(fpath,'w') as f:
        f.write(" ".join(tmp)+"\n")
    return True
def saveImg(localId,issue):
    imgSavePath = OSS_IMG / str(localId)
    if not imgSavePath.exists():
        imgSavePath.mkdir()

    if  docker_save(f"arvo/{localId}-vul",(imgSavePath / f"{localId}-vul.tar").absolute())==True and \
        docker_save(f"arvo/{localId}-fix",(imgSavePath / f"{localId}-fix.tar").absolute())==True and \
        docker_rmi(f"arvo/{localId}-vul")== True and \
        docker_rmi(f"arvo/{localId}-fix")== True and \
        saveCommand(imgSavePath/f"arvo_vul.sh",f"arvo/{localId}-vul",issue) and \
        saveCommand(imgSavePath/f"arvo_fix.sh",f"arvo/{localId}-fix",issue):
        return True
    else:
        shutil.rmtree(imgSavePath)
        return False

def verify(localId,save_img=False):
    # if Save_img == True, we should make sure there is no two workers working
    # on the same localId or confliction may happen
    print(localId)

    built_img = False
    if save_img==True:
        docker_rmi(f"arvo/{localId}-vul")
        docker_rmi(f"arvo/{localId}-fix")
    def leave(result):
        if save_img == True:
            docker_rm(f"reproducer_{localId}")
            if result == False:
                docker_rmi(f"arvo/{localId}-vul")
                docker_rmi(f"arvo/{localId}-fix")
        if CLEAN_TMP and case_dir:
            clean_dir(case_dir)
        if RM_IMAGES and built_img:
            try:
                remove_oss_fuzz_img(localId)
            except:
                pass
        return result
    srcmap,issue = getIssueTuple(localId)
    if not srcmap or not issue:
        eventLog(f"Failed to get the srcmap or issue for case {localId}")
        return False
    if 'project' not in issue.keys():
        issue['project'] = issue['fuzzer'].split("_")[1]
    case_dir = tmpDir()
    print("[+] Downloading PoC")
    try:
        case_path = download_reproducer(issue,case_dir,"crash_case")
    except:
        issue_record(issue['project'],localId,f"Fail to Download the Reproducer")
        return leave(False)
    if not case_path or not case_path.exists():
        issue_record(issue['project'],localId,f"Fail to Download the Reproducer")
        return leave(False)
    if(len(srcmap)!=2):
        issue_record(issue['project'],localId,f"Have more/less than 2 Scrmap")
        return leave(False)
    old_srcmap =  srcmap[0]
    new_srcmap =  srcmap[1]
    print("[+] Build the Vulnerable Version")
    if save_img == True:
        old_res = build_from_srcmap(old_srcmap,issue,save_img="Vul")
    else:
        old_res = build_from_srcmap(old_srcmap,issue)
    if not old_res:
        issue_record(issue['project'],localId,f"Fail to build old fuzzers from srcmap")
        return leave(False)
    built_img = True
    ret_code = crashVerify(issue,case_path)
    if ret_code==None:
        issue_record(issue['project'],localId,f"Fail to get the fuzzer")
        return leave(False)
    if ret_code:
        issue_record(issue['project'],localId,f"Fail to reproduce the crash")
        return leave(False)
    if save_img == True:
        if not docker_cp(case_path.absolute(),f"reproducer_{localId}:"+"/tmp/poc"):
            return leave(False)
        if not doCommitNclean(localId,'vul'):
            return leave(False)
     
    print("[+] Build the Fixed Version")
    if save_img != True:
        remove_oss_fuzz_img(localId) # Remove docker image
    built_img = False
    if save_img == True:
        new_res = build_from_srcmap(new_srcmap,issue,save_img="Fix")
    else:
        new_res = build_from_srcmap(new_srcmap,issue)
    if not new_res:
        issue_record(issue['project'],localId,f"Fail to build new fuzzers from srcmap")
        return leave(False)
    built_img = True
    ret_code = crashVerify(issue,case_path)
    if not ret_code:
        issue_record(issue['project'],localId,f"Fail to reproduce the fix")
        return leave(False)
    if save_img == True:
        if not docker_cp(case_path.absolute(),f"reproducer_{localId}:"+"/tmp/poc"):
            return leave(False)
        if not doCommitNclean(localId,'fix'):
            return leave(False)
        if saveImg(localId,issue)==False:
            return leave(False)    
    return leave(True)

def doCommitNclean(localId,tag):
    if not docker_commit(f"reproducer_{localId}",f"arvo/{localId}-{tag}"):
        return False
    if not docker_rm(f"reproducer_{localId}"):
        return False
    if not docker_rm(f"arvo_deamon_{localId}"):
        return False
    return True
        
if __name__ == "__main__":
    pass