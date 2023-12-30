from utils_exec import check_call
import shutil
import os
from utils import tmpDir, tmpFile, eventLog
class GitTool():
    def __init__(self,oriRepo) -> None:
        if not oriRepo.exists():
            eventLog(f"[-] GitTool: The original repo doesn't exists:\n{oriRepo}\n")
            exit(1)
        else:
            self.repo = oriRepo
            self.name = self.repo.name
    def copy(self):
        try:
            org = self.repo
            new = tmpDir()
            shutil.copytree(org,new/self.name,symlinks=True)
            self.repo = new/self.name
            return True
        except:
            return False
    def reset(self,commit):
        if self.copy() == False: # so we will not pollute the original repo
            return False
        cmd = ['git','reset','--hard',commit]
        return check_call(cmd,self.repo)
    def listCommits(self,commit1,commit2):
        
        # commit1 should be elder
        # return a list includes commits between [commit1, commit2] (including commit1 and commit2)
        # but not include branch nodes
        tmp_file = tmpFile()
        cmd = ['git','log',f"{commit1}..{commit2}",'--pretty=format:%H']
        print(" ".join(cmd))
        if not check_call(cmd,self.repo,stdout=open(tmp_file,'w')):
            return False
        with open(tmp_file) as f:
            res = [x.strip() for x in f.readlines()]
        shutil.rmtree(os.path.dirname(tmp_file))
        res.append(commit1)
        return res[::-1]
    def showCommit(self,commit):
        # return the path of the diff file
        tmp_file = tmpFile()
        # -W to show the whole function
        # -m for merged commits
        # add timeout to avoid spending too much time on merging diff
        cmd = ['timeout','30','git','show','--diff-merges=first-parent','-W',commit]
        print(commit)
        if check_call(cmd,self.repo,stdout=open(tmp_file,'w'),stderr=open("/dev/null",'w')):
            return tmp_file
        # cmd = ['timeout','30','git','show','-W',commit]
        # if check_call(cmd,self.repo,stdout=open(tmp_file,'w')):
            # return tmp_file
        return False
        
    def prevCommit(self,commit=None):
        # reutrn the previous commit hash
        tmp_file = tmpFile()
        cmd = ['git','log','-2','--pretty=format:%H']
        if commit != None:
            cmd.append(commit)
        if not check_call(cmd,self.repo,stdout=open(tmp_file,'w')):
            return False
        with open(tmp_file) as f:
            res = [x.strip() for x in f.readlines()][-1]
        shutil.rmtree(os.path.dirname(tmp_file))
        return res

if __name__ == "__main__":
    pass