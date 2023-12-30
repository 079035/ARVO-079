# Functions to Fx Test
# The Fx test should not be multi threads
from fx import *
from os import remove
def _updateLog(localId,result,log_file):
    d = dict()
    d[localId] = result
    with open(log_file,'a') as f:
        f.write(json.dumps(d)+"\n")
def _loadLog(log_file):
    with open(log_file) as f:
        lines  = f.readlines()
    return [ int(x.split('":')[0][2:]) for x in lines[4:]]
def _updateTodo(todo, log_file):
    done = _loadLog(log_file)
    todo = [ x for x in todo if x not in done]
    return todo

def fxProbeTurbo(localIds,model,round_tag,tag="",lite=False):
    log_file = Path("./Data/Data") / round_tag / ("n132FxLog_"+model+"_"+tag)
    print(log_file)
    if log_file.exists():
        pass
    else:
        log_file.touch()
        # Head
        with open(log_file,'w') as f:
            tmp = [str(x) for x in localIds]
            tmp = " ".join(tmp)
            f.write(f"LocalIds: {tmp}\n")
            f.write(f"Time: {datetime.now()}\n")
            f.write(f"Model: {model}\n")
            f.write("="*0x20)
            f.write("\n")
    todo = _updateTodo(localIds,log_file)
    # Body
    while len(todo) > 0:
        localId = random.choice(todo)
        print(f"[+] Verfiying {localId}")
        
        flock = OSS_LOCK / f"{localId}"
        if flock.exists():
            print(f"[+] A process is working on {localId}")
            sleep(0x20)
            todo = _updateTodo(localIds,log_file)
            continue
        
        flock.touch()
        if 1:
            res = XxX(localId,model,1,lite,Path("./Data/Data") / round_tag,tag=tag)
        #except:
         #   res = False
        remove(flock)

        _updateLog(localId,res,log_file)
        todo = _updateTodo(localIds,log_file)

    # Tail
    print(f"[+] Model {model} has finished running.")
    print(log_file)



if __name__ == "__main__":
    pass