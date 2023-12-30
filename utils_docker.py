import re
import subprocess
import os
from base58 import b58encode
from utils_exec import *
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
    print("[+] Docker Run: \n"+" ".join(cmd))
    return check_call(cmd)
def docker_cp(arg1,arg2):
    cmd = ['docker','cp',arg1,arg2]
    return check_call(cmd)
def docker_images(name):
    cmd = ["docker","images","-aq",name]
    return execute(cmd).decode()
def docker_rmi(img_name):
    target_hash = docker_images(img_name)
    if target_hash== "":
        return True
    cmd = ['docker','rmi',target_hash]
    return check_call(cmd)
def docker_ps(container_name):
    cmd = ["docker", "ps", "-aq", "-f", f"name={container_name}"]
    return execute(cmd).decode()
def docker_commit(container_name,image_name):
    cmd = ['docker','commit',container_name,image_name]
    return check_call(cmd)
def docker_rm(container_name):
    target_hash = docker_ps(container_name)
    if target_hash == "":
        return True
    cmd = ['docker','stop',target_hash]
    with open('/dev/null','w') as f:
        if check_call(cmd,stdout=f,stderr=f):
            target_hash = docker_ps(container_name)
            if "\n" in target_hash:
                target_hash = target_hash.split("\n")
                cmd = ['docker','rm']+target_hash
            else:
                if target_hash == "":
                    return True
                cmd = ['docker','rm',target_hash]
            return check_call(cmd,stdout=f,stderr=f)
        else:
            return False
def docker_save(img_name,output_name):
    output_name = str(output_name)
    with open('/dev/null','w') as f:
        cmd = ['docker','save',"-o", output_name , img_name]
        return check_call(cmd,stdout=f,stderr=f)
def docker_build(args):
    cmd = ['docker','build']
    cmd.extend(args)
    print("[+] Docker Build: \n"+" ".join(cmd))
    return check_call(cmd)
def docker_load(instream):
    cmd = ['docker','load']
    print("[+] Docker Load: \n"+" ".join(cmd))
    return check_call(cmd,stdin=instream)
def docker_exec(container: str,command: list):
    cmd = ['docker','exec',container]+command
    print("[+] Docker Exec: \n"+" ".join(cmd))
    with open('/dev/null','w') as f:
        return check_call(cmd,stdout=f,stderr=f)