import re
import subprocess
from utils_exec import check_call
class DfTool():
    def __init__(self,path) -> None:
        self.path = path
        with open(path) as f:
            self.content = f.read()
    def panic(self,s):
        print(f"[-] {s}")
        exit(1)
    def writeDf(self):
        try:
            with open(self.path,'w') as f:
                f.write(self.content)
        except:
           return False
        return True
    def replace(self,old,new):
        self.content = re.sub(old,new,self.content)
        return self.writeDf()
    def insertLineAfrer(self,target,newline):
        assert(type(newline)==str)
        assert(type(target)==str)
        if target[-1]!='\n':
            target = target+'\n'
        if newline[-1] !='\n':
            newline= newline+'\n'
        if len(re.findall(target,self.content))==0:
            self.panic(f"Failed to locate the line: {target[:0x10]}...")
        else:
            self.content = self.content.replace(target,target+newline)
        return self.writeDf()
    def insertLineBefore(self,target,newline):
        assert(type(newline)==str)
        assert(type(target)==str)
        
        target = target+'\n' if target[-1]!='\n' else target 
        newline= newline+'\n' if newline[-1] !='\n' else newline 
        if len(re.findall(target,self.content))==0:
            self.panic(f"Failed to locate the line: {target[:0x10]}...")
        else:
            self.content = self.content.replace(target,newline+target)
        return self.writeDf()
    def insertLineat(self,pos,line):
        assert(type(line)==str)
        line = line+'\n' if line[-1]!='\n' else line 
        lines = self.content.split("\n")
        lines.insert(pos,line)
        self.content = "\n".join(lines)
        return self.writeDf()
    def dump(self):
        print("[+] Dumping the Content")
        print(self.content)

# Docker Options
def docker_login():
    res = subprocess.run(["docker","login"])
    return res.returncode
def docker_run(args,rm=True):
    if rm:
        cmd = ['docker','run','--rm','--privileged']
    else:
        cmd = ['docker','run','--privileged']
    cmd.extend(args)
    print("[+] Docker Run: \n\n"+" ".join(cmd)+"\n\n")
    return check_call(cmd)
def docker_cp(arg1,arg2):
    cmd = ['docker','cp',arg1,arg2]
    return check_call(cmd)
def docker_rmi(img_name):
    cmd = ['docker','rmi',img_name]
    return check_call(cmd)
def docker_commit(container_name,image_name):
    cmd = ['docker','commit',container_name,image_name]
    return check_call(cmd)
def docker_stop_and_rm(container_name):
    cmd = ['docker','stop',container_name]
    if check_call(cmd):
        cmd = ['docker','rm',container_name]
        return check_call(cmd)
    else:
        return False
def docker_save(img_name,output_name):
    cmd = ['docker','save',"-o", output_name , img_name]
    return check_call(cmd)
def docker_build(args):
    cmd = ['docker','build']
    cmd.extend(args)
    print("[+] Docker Build: \n\n"+" ".join(cmd)+"\n\n")
    return check_call(cmd)
