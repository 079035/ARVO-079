# This script is used for commiting the successful cases. 
# Since we found that some cases are not stable, for example
# we reproduced a case two months ago, but we can't reproduce it now.
# To make sure others can easily reproduce it, we'll commit the successful cases
# ---------------------------------------------------
# Procedure:
#    Try to reproduce
#    if (Success):
#           commit the compiled files (include the everything on the container)
#    else:
#           mark the case as not stable
# Intro:
#     1. This method is also not stable for people who want to modify the code and recompile
#                           because the compile-script may need to download some resource from internet, which can be removed/modified
#     2. For people only want do testing on the binary, it's a great resource!

# ---------------------------------------------------
from unitTest import *
from report_gen import *

def _docker_commit(localId):
    print(localId)
    def leave(result):
        if CLEAN_TMP and case_dir:
            clean_dir(case_dir)
        if(RM_IMAGES):
            remove_oss_fuzz_img(localId)
        if result == False:
            try:
                docker_rmi("oss_reproducer/{localId}_vul")
            except:
                pass
            try:
                docker_rmi("oss_reproducer/{localId}_fix")
            except:
                pass
        return result
    srcmap,issue = getIssueTuple(localId)
    if not srcmap or not issue:
        exit(1)
    case_dir = tmpDir()
    try:
        case_path = download_reproducer(issue, case_dir, "crash_case")
    except:
        return leave(False)
    if not case_path or not case_path.exists():
        return leave(False)
    if(len(srcmap)==2):
        old_srcmap =  srcmap[0]
        new_srcmap =  srcmap[1]
        old_res = build_from_srcmap(old_srcmap,issue,commit_build=True,more_info={"localId":localId,"fix":False})
        if not old_res:
            return leave(False)
        ret_code = crash_verfiy(issue,case_path)
        if ret_code==None:
            return leave(False)
        if(docker_cp(str(case_path),f"reproducer_{localId}:"+"/tmp/reproducer_poc")!=True or \
                docker_commit(f"reproducer_{localId}",f"oss_reproducer/{localId}_vul")!=True or \
                docker_stop_and_rm(f"reproducer_{localId}")!=True):
            leave(False)
        if ret_code:
            return leave(False)
        new_res = build_from_srcmap(new_srcmap,issue,commit_build=True,more_info={"localId":localId,"fix":True})
        if not new_res:
            return leave(False)
        ret_code = crash_verfiy(issue,case_path)
        if not ret_code:
            return leave(False)
        if(docker_cp(str(case_path),f"reproducer_{localId}:"+"/tmp/reproducer_poc")!=True or \
            docker_commit(f"reproducer_{localId}",f"oss_reproducer/{localId}_fix")!=True or \
            docker_stop_and_rm(f"reproducer_{localId}")!=True):
            leave(False)
        return leave(True)
    else:
        return leave(False)
def docker_commit(localId):
    res = _docker_commit(localId)
    if(DOCKER_COMMIT_LOG == False):
            return res
    if(res):
        res = "True"
    else:
        res = "False"
    with open("./_DOCKER_COMMIT_LOG_REPRODUCE.log",'a') as f:
        f.write(f"[{res}]\t\t\t: {localId}\n")
    return res

if __name__ == "__main__":
    DOCKER_COMMIT_LOG = True
    reports = GET_REPORT()
    ct = 0 
    for x in reports:
        res = docker_commit(x)
        ct+=1
        if(ct==33):
            exit(1)
