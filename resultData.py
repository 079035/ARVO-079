from utils import *
RESULTS = Path(oss_reproducer_dir) / "Results.json"

'''
        Matric
        These functions are used to maintain RESULTS file
'''
def matric_lookup(localId):
    with open(RESULTS,'r') as f:
        data = f.readlines()
    for x in data:
        if localId == json.loads(x)['localId']:
            return True
    return False
def matric_ins(localIds,results):
    f = open(RESULTS,'a+')
    assert(len(localIds)==len(results))
    for x in range(len(localIds)):
        issue = getIssue(localIds[x])
        payload = {}
        payload['localId'] = localIds[x]
        payload['project'] = issue['project']
        payload['pass'] = results[x]
        f.write(json.dumps(payload)+'\n')
    f.close()
    return 
def matric_del(l):
    data = matric_raw()
    res = []
    for x in range(len(data)):
        if data[x]['localId'] not in l:
            res.append(data[x])
    res = [json.dumps(x)+"\n" for x in res]
    with open(RESULTS,'w') as f:
        f.writelines(res)
    return res
def matric_raw():
    with open(RESULTS,'r') as f:
        data = f.readlines()
    rec = []
    for x in data:
        rec.append(json.loads(x))
    return rec
def matric_true():
    data = matric_raw()
    res = []
    for x in data:
        if x['pass']:
            res.append(x['localId'])
    return res
def matric_sort(key="localId"):
    def _cmp2(x):
        return json.loads(x)['project']
    def _cmp1(x):
        return json.loads(x)['localId']
    with open(RESULTS,'r') as f:
        data = f.readlines()
    print(len(data))
    data = list(set(data))
    print(len(data))
    if key == "project":
        data.sort(key=_cmp2)
    else:
        data.sort(key=_cmp1)
    with open(RESULTS,'w') as f:
        f.writelines(data)
    return