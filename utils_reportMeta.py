import json
def reportName2localId(name):
    return int(name.split("/")[-1][:-5])
def getReportMeta(localId):
    with open("./Reports/"+str(localId)+".json") as f:
        meta = json.loads(f.read())
    return meta

