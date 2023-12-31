import subprocess
from pathlib import Path
def execute(cmd,cwd=None):
    if not cwd:
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
    else:
        p = subprocess.Popen(cmd,cwd = cwd,stdout=subprocess.PIPE)
    out,_ = p.communicate()
    return out.strip()
def execute_ret(cmd,cwd=None,stdin=None,stdout=None,stderr=None):
    if not cwd:
        p = subprocess.Popen(cmd,stdin=stdin,stdout=stdout,stderr=stderr)
    else:
        p = subprocess.Popen(cmd,cwd =cwd,stdin=stdin,stdout=stdout,stderr=stderr)
    __,_ = p.communicate()
    return p.returncode
def check_call(cmd,cwd=Path("/tmp"),stdin=None,stdout=None,stderr=None):
    try:
        subprocess.check_call(cmd,stdin=stdin,stdout=stdout,stderr=stderr,cwd=cwd) 
    except:
        cmd = " ".join(cmd)
        print(f"[!] Failed to execute the command:\n```\n{cmd}\n```\nWorkdir:\n{cwd}")
        return False
    return True