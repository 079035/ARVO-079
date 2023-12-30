# Functions to Reproduction Test
import json
from pathlib import Path
import random
from time import sleep
from utils import OSS_LOCK
from os import remove
from reproducer import verify
def removeSucceed(issues):
    with open("Results.json") as f:
        data = f.readlines()
    done    = [json.loads(x)['localId'] for x in data]
    return [_  for _ in issues if _ not in done]
def touchLogfile(log_file):
    log_file = Path(log_file)
    if not log_file.exists():
        log_file.touch()
    return log_file
def updateLogfile(localid,res,log_file):
    tmp = dict()
    tmp[localid] = res
    with open(log_file,'a') as f:
        f.write(json.dumps(tmp)+"\n")
def updateTodo(issues,log_file):
    with open(log_file,'r') as f:
        done = [ int(list(json.loads(x).keys())[0]) for x in f.readlines()]
    return [_  for _ in issues if _ not in done]
def unitExplore(issues,log_file,remove_result=True):
    log_file    = touchLogfile(log_file)
    if remove_result:
        issues      = removeSucceed(issues)
    todo        = updateTodo(issues,log_file)
    while len(todo)> 0 :
        choice = random.choice(todo)
        print(f"[+] Verfiying {choice}")
        print(f"[+] {len(todo)} issues left")
        res = verify(choice)
        updateLogfile(choice,res,log_file)
        todo = updateTodo(issues,log_file)
def archive(issues,log_file):
    log_file    = touchLogfile(log_file)
    todo        = updateTodo(issues,log_file)
    while len(todo)> 0 :
        choice = random.choice(todo)
        print(f"[+] Verfiying {choice}")
        print(f"[+] {len(todo)} issues left")
        flock = OSS_LOCK / f"{choice}"
        if flock.exists():
            print(f"[+] A process is working on {choice}")
            sleep(0x20)
            continue
        else:
            flock.touch()
        res = verify(choice,True)
        remove(flock)
        updateLogfile(choice,res,log_file)
        todo = updateTodo(issues,log_file)

def extractSucceedIssues(log_file):
    with open(log_file,'r') as f:
        res = [ int(list(json.loads(x).keys())[0]) for x in f.readlines() if list(json.loads(x).values())[0]== True]
    res = list(set(res))
    return res

if __name__ == "__main__":
    pass