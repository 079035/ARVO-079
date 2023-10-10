from pathlib import Path
import _profile
import json
import shutil
from time import sleep
from base58 import b58encode
OSS_DB      = Path(_profile.OSS_DB_DIR)
OSS_DB_MAP  = OSS_DB/"map"
RETRY       = 4
import _profile 
def eventLog(s):
    with open(Path(_profile.oss_reproducer_dir)/"Log"/"_Event.log",'a') as f:
        f.write(s+"\n")
def DB_DUMP(rec):
    ct = 0 
    while ct < RETRY:
        try:
            with open(OSS_DB_MAP,'w') as f:
                f.write(json.dumps(rec,indent=4))
            return True
        except:
            sleep(0.3)
            ct+=1
    return False
def DB_INSERT(url,orig):
    if not orig.exists():
        return False
    rec = DB_MAP()
    if url in rec.keys():
        del rec[url]
    dest = OSS_DB /  b58encode(url).decode()        
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir()
    try:
        shutil.copytree(orig,dest/orig.name,symlinks=True)
    except:
        return False
    rec[url] = str(dest/orig.name)
    if not DB_DUMP(rec):
        eventLog("[!] DB_INSERT: OSS_DB is polluted")
        exit(1)
    else:
        return True


def DB_CHECK(url):
    map = DB_MAP()
    if url in map.keys():
        res = Path(map[url])
        if res.exists():
            return res
        else:
            DB_remove(url,res)
            return False
    else:
        return False
def DB_MAP():
    ct = 0 
    while ct < RETRY*2:
        try:
            with open(OSS_DB_MAP) as f:
                res = json.loads(f.read())
            return res
        except:
            sleep(0.3)
            ct+=1
    eventLog("[!] DM_MAP: Failed to get DB MAP")
    exit(1)
def DB_remove(url,path):
    if path.exists():
        shutil.rmtree(path)
    data = DB_MAP()
    try:
        del data[url]
    except:
        pass
    with open(OSS_DB_MAP,'w') as f:
        f.write(json.dumps(data,indent=4))
    