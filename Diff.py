from utils import *
from n132 import *
from utils_reportMeta import *
from utils_git import *
from Locator import report
def _prepare_repo(localId):
    print(f"[+] Preparing the repo for issue: {localId}")
    meta    = getReportMeta(localId)
    url     = meta['repo_addr']
    target_dir = DB_CHECK(url)
    if target_dir == False:
        tmp = clone(url)
        if tmp ==False:
            report(localId)
            tmp = clone(url)
        if tmp ==False:
            target = str(Path(oss_reproducer_dir)/"Reports"/f"{localId}.json")
            os.system(f"rm -rf {target}")
            eventLog(f"_prepare_repo: Fail to clone repo: {localId}")
            return False
        shutil.rmtree(tmp)
        target_dir = DB_CHECK(url)     
        if target_dir == False:
            eventLog(f"_prepare_repo: Fail to clone repo: {localId}")
            exit(1)
    return target_dir
def getVulCommit(localId):
    # return the previous commit of the fix
    commit  = getReportMeta(localId)['fix_commit']
    repo    = _prepare_repo(localId)
    if repo == False:
        return False
    gt = GitTool(repo)
    return gt.prevCommit(commit)
def getDiff(localId):
    commit  = getReportMeta(localId)['fix_commit']
    repo    = _prepare_repo(localId)
    if repo == False:
        return False
    gt = GitTool(repo)
    return gt.showCommit(commit)
if __name__ == "__main__":
    pass