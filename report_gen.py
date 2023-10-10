import json
from glob import glob
from Locator import report
import random
from pathlib import Path

REPORT_LOG = "./_REPORT_GEN.log"
if not Path(REPORT_LOG).exists:
    print(f"[!] Report_gen: {REPORT_LOG} doesn't exists")
    exit(1)
def GET_ISSUE():
    with open("./Results.json",'rb') as f:
        data= f.readlines()
    return [ json.loads(x)["localId"] for x in data if json.loads(x)["pass"]]
def GET_REPORT():
    return [int(x[10:-5]) for x in glob("./Reports/*")]
def GET_LOGS():
    existing = Path("./Reports/").glob("*.json")
    return set([int(x.name[:-5]) for x in existing])
def DUMP_LOG(case,result):
    with open(REPORT_LOG,'a') as f:
        f.write(f"{case}: {result}\n")
def GET_LOG():
    with open(REPORT_LOG,'r') as f:
        return [ int(x.strip().split(": ")[0]) for x in f.readlines()]
    
if __name__ == '__main__':
    issues  = GET_ISSUE()
    reports = GET_REPORT()
    issues  = [ x for x in issues if x not in reports]
    done = GET_LOG()
    while any(_ not in done for _ in issues):
        choice = random.choice(issues)
        if choice in done:
            continue    
        try:
            res = report(choice)
        except:
            res = False
        DUMP_LOG(choice,res)
        done = GET_LOG()