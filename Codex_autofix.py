# This script only chose the vulnerabilities that can be fixed easily

import json
from fx import XxX

statistics = "./Data/FixMeta.json"
def get_targets():
    with open(statistics) as f:
        lines = f.readlines()
    lines = [ json.loads(x) for x in lines]
    lines = [x for x in lines if x[next(iter(x))]['Modification']==1]
    res = [int(next(iter(x))) for x in lines]
    # print(res)
    return res
def fixing(targets):
    return [ XxX(x) for x in targets]


if __name__ =="__main__":
    targets = get_targets()
    for x in targets:
        res = XxX(x)
        with open("_CODEX_AUTOFIX_LOG.log",'a+') as f:
            f.write(f"{x}: {res}\n")