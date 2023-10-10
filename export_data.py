# Use to deal with the data of fix
import json 
import pandas as pd
import collections

from utils_GPT    import *
from utils          import *
from glob           import glob
from pathlib        import Path

START_DATE = '2016-08' 
END_DATE = '2023-09'

def _get_year(d):
    return int(d[:4])

def _get_month_diff(start, end):
    sy = _get_year(start)
    ey = _get_year(end)
    sm = int(start[5:])
    em = int(end[5:])
    dif = 0
    if ey>sy:
        dif += (ey-sy)*12
        if sm>em:
            dif -= 12
            dif += 12-abs(em-sm)
        else:
            dif += 12-abs(em-sm)
    else:
        dif += abs(em-sm)
    return dif

# Get verified cases from Results.json's git commits (# of added cases)
def _get_reproducible_cases():
    cases = []
    with open('./Results.json') as f:
        for line in f:
            data = json.loads(line)
            if data['pass']==True:
                cases.append(data['localId'])
    return cases

def group_by_month(d, unit_month):
    trend = list(d.items()) # convert dictionary to tuple
    pivot = START_DATE      # this one moves
    organized = [0]         # will be separated by unit months
    for c in trend:
        diff = _get_month_diff(pivot, c[0])
        # print(c[0])
        # print(diff)
        if diff < unit_month:
            organized[-1] += c[1]
        else:
            for i in range(0, diff-1):
                organized.append(organized[-1])
            organized.append(organized[-1] + c[1])
            pivot = c[0]
    for i in range(_get_month_diff(trend[-1][0], END_DATE)):
        organized.append(organized[-1])
    return organized

def organize_data():
    bug_trend = {} # All bugs besides below two
    rep_trend = {} # Reproducible
    fix_trend = {} # Easy fixes
    # print("[*] Getting single mods (easy fixes)")
    # single_mods = _get_all_single_mods(True)
    # sm = [38843, 6214, 45884, 12684, 37334, 20491, 28953, 340, 39070, 8511, 6066, 7361, 8317, 14912, 3658, 6626, 24854, 5832, 9180, 3522, 11074, 22244, 3956, 28654, 31038, 31556, 10953, 31124, 25545, 4822, 33663, 5568, 40589, 5710, 8529, 21356, 40617, 26442, 10724, 33576, 35342, 5296, 6899, 4099, 10356, 30113, 20800, 5935, 30831, 37759, 10762, 14423, 44089, 21309, 27279, 31425, 1304, 11290, 3559, 26171, 5362, 23396, 28392, 3645, 7171, 8316, 37222, 25226, 39103, 4296, 19386, 37158, 4819, 38924, 3257, 6243, 40429, 5381, 29821, 22169, 6829, 21070, 28682, 4637, 6906, 8241, 30748, 46309, 19324, 11429, 39664, 38898, 26755, 13016, 33841, 338, 13467, 32275, 20363, 39036, 12642, 11245, 5577, 391, 21349, 22864, 33843, 23826, 13531, 35300, 37575, 3265, 43370, 3474, 4345, 3621, 33071, 31065, 4561, 3862, 7538, 12871, 5534, 35297, 27812, 12818, 11011, 3322, 17147, 37866, 5729, 5429, 35288, 3938, 420, 4300, 14393, 38146, 30974, 10990, 27816, 12241, 32177, 14854, 5499, 42741, 7262, 6975, 5372, 16445, 11060, 4670, 12549, 10081, 10881, 5652, 5373, 910, 5547, 40269, 27368, 39053, 919, 5482, 25973, 4440, 14018, 3376, 7206, 5504, 346, 21348, 8505, 36611, 39102, 5576, 31586, 3447, 14035, 12312, 10082, 4764, 14331, 21296, 38900, 12552, 15603, 5761, 31552, 10097, 22912, 30293, 3530, 11351, 3497, 4569, 12787, 28315, 5326, 5481, 4346, 22498, 24293, 18877, 31585, 14481, 7884, 5443, 31454, 11305, 10955, 5498, 37564, 12532, 18756, 39056, 38237, 8616, 5256, 4396, 19332, 5480, 1856, 6831, 3680, 12631, 4289, 37647, 5740, 3371, 3498, 4812, 39028, 11376, 39094, 3285, 10084, 5843, 42729, 5873, 26406, 38121, 12679, 19100, 22167, 6790, 33264, 34259, 3558, 29816, 40431, 6007, 39083, 3560, 37878, 5450, 31551, 19338, 25118, 37211, 31535, 33863, 21346, 38341, 12536, 31705]
    reproducibles = _get_reproducible_cases()
    # print(len(reproducibles))
    # single_mods = [f for f in sm if f not in reproducibles]
    # print(reproducibles)
    # print(len(single_mods))   # 266
    with open('./Type.Bug-Security_label.Reproducible_status.Verified/metadata.jsonl.new') as f:
        for line in f:
            data = json.loads(line)
            timestamp = datetime.fromtimestamp(data['issue']['statusModifiedTimestamp']).strftime("%Y-%m")
            localId = data['localId']
            if localId in reproducibles:
                try:
                    rep_trend[timestamp] += 1
                except KeyError as e:
                    rep_trend[timestamp] = 1
            # elif localId in single_mods:
            #     try:
            #         fix_trend[timestamp] += 1
            #     except KeyError as e:
            #         fix_trend[timestamp] = 1
            else:
                try:
                    bug_trend[timestamp] += 1
                except KeyError as e:
                    bug_trend[timestamp] = 1
    # fix_sorted = collections.OrderedDict(sorted(fix_trend.items()))
    rep_sorted = collections.OrderedDict(sorted(rep_trend.items()))
    bug_sorted = collections.OrderedDict(sorted(bug_trend.items()))
    # print(rep_sorted)
    # print(sum(rep_sorted.values()))
    return rep_sorted, bug_sorted

# save db size growth data to csv
def export_reproduce_data(unit_month = 1):
    reproducible, all_bugs = organize_data()
    dates = pd.date_range(START_DATE, END_DATE, freq=str(unit_month)+'MS').strftime("%Y-%m").tolist()
    # print(reproducible)
    # print(all_bugs)
    rep_organized = group_by_month(reproducible, unit_month)
    # fix_organized = group_by_month(easy_fixes, unit_month)
    bug_organized = group_by_month(all_bugs, unit_month)
    # print(rep_organized)
    # print(bug_organized)
    # print(len(rep_organized))
    # print(len(bug_organized))
    assert(len(rep_organized) == len(bug_organized))
    
    print("Reproducible cases by month: ",end='')
    print(rep_organized)
    # print("Single fix cases by month: ",end='')
    # print(fix_organized)
    print("All bug-related cases by month: ",end='')
    print(bug_organized)
    
    df = pd.DataFrame({'Date':dates, 'Reproducible':rep_organized})
    # df = df.join(pd.DataFrame({'Easy Fixes':fix_organized}))
    df = df.join(pd.DataFrame({'All Bugs':bug_organized}))
    print(df)
    
    ### export to csv
    df.to_csv(r'./Data/dbsize.csv', index=False)
    print("[+] Exported to dbsize.csv")

def _get_proj_lang(proj_name):
    dirnames = glob("../oss-fuzz/projects/*")
    # print(dirnames)
    for p in dirnames:
        if p.split("/")[-1] == proj_name:
            info = Path(p)/"project.yaml"
            if info.exists():
                with open(info) as f:
                    lines = f.readlines()
                for line in lines:
                    dt = line.strip().split(": ")
                    if dt[0] == "language":
                        if dt[1].startswith('"'):
                            dt[1] = dt[1][1:-1] 
                        return dt[1]
    return ''

def get_lang_dist():
    dirnames = glob("../oss-fuzz/projects/*")
    # print(dirnames)
    bug_dist = dict()
    for _ in dirnames:
        info = Path(_)/"project.yaml"
        if info.exists():
            with open(info) as f:
                lines = f.readlines()
            for line in lines:
                dt = line.strip().split(": ")
                if dt[0] == "language":
                    if dt[1].startswith('"'):
                        dt[1] = dt[1][1:-1] 
                    if dt[1] not in bug_dist:
                        bug_dist[dt[1]] = 1
                    else:
                        bug_dist[dt[1]] +=1 
        else:
            print(f"{info} doesn't exist, skiping...")
    print(bug_dist)  # all bugs lang distribution
    
    langs = dict()
    proj_map = dict()
    with open('./Results.json') as f:
        for line in f:
            data = json.loads(line)
            if data['pass']=='false':
                continue
            proj_name = data['project']
            if proj_name in proj_map:
                continue
            proj_map[proj_name] = 1
            proj_lang = _get_proj_lang(proj_name)
            if proj_lang not in langs:
                langs[proj_lang] = 1
            else:
                langs[proj_lang] += 1
    print(langs)
    
    res = dict()
    for l in langs:
        if l in bug_dist:
            res[l] = langs[l]/bug_dist[l]
    print(res)
    return res

def export_lang_dist():
    dist = get_lang_dist()
    df = pd.DataFrame({'Language':list(dist.keys()), 'Reproducible':list(dist.values())})
    print()
    print(df)
    df.to_csv(r'./Data/langdist.csv', index=False)
    print("[+] Exported to langdist.csv\n")
    
def reproduce_vs_google():
    local = [False, False, False, False, False, False, True, False, False, True, False, False, True, False, False, False, True, True, False, False, False, False, True, False, False, True, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, False, False, False, False, False, True, True, False, False, False, False, False, True, True, False, True, False, True, False, False, False, False, False, False, True, True, False, False, False, False, False, False, False, False, True, True, False, False, True, False, False, False, False, False, False, False, False]
    # print(len(local))
    google = [False]*40+ [True]*2+[False]*40+[True]*3+[False]*15
    # print(len(google))
    assert len(local) == len(google)
    n = len(local)
    res_local = [1 if local[0]==True else 0]
    res_google = [1 if google[0]==True else 0]
    for i in range(1,n):
        if local[i]==True:
            res_local.append(res_local[-1]+1)
        else:
            res_local.append(res_local[-1])
        if google[i]==True:
            res_google.append(res_google[-1]+1)
        else:
            res_google.append(res_google[-1])
    print(res_local)
    print(res_google)
    col = [i for i in range(1,n+1)]
    df = pd.DataFrame({'Case':col, 'OSS Reproducer':res_local})
    df = df.join(pd.DataFrame({'Google':res_google}))
    df.to_csv(r'./Data/vsgoogle.csv', index=False)
    print("[+] Exported to vsgoogle.csv\n")
    

if __name__ =="__main__":
    reproduce_vs_google()
    export_lang_dist()
    export_reproduce_data()