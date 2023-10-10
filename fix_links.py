import json 
from glob           import glob

def _get_report(localId):
    with open("./Reports/"+str(localId)+".json") as f:
        meta = json.loads(f.read())
    return meta

def _get_reports_id():
    res = glob("./Reports/*")
    return [int(x.split("/")[-1][:-5]) for x in res]

def fix_links():
    reports = _get_reports_id()
    print("There are "+str(len(reports))+" reports")
    kinds = {}
    ids = {}
    
    # run analytics
    for localID in reports:
        r = _get_report(localID)
        fix_link = r['fix']
        domain = fix_link.split("/")[2]
        try:
            kinds[domain] += 1
        except KeyError as e:
            kinds[domain] = 1
        try:
            ids[domain].append(localID)
        except KeyError as e:
            ids[domain] = []
            ids[domain].append(localID)
    for key in kinds:
        print(str(key) + ": "+str(kinds[key])+"\n"+str(ids[key]))
        print()
        
    
    # fix links
    for localID in reports:
        r = _get_report(localID)
        fix_link = r['fix']
        link = fix_link.split("/")
        domain = link[2]
        
        if domain == "github.com": # Fix github commit links
            link[-2] = "commit"
            fix_link = '/'.join(link)
            r['fix'] = fix_link
            with open(f'./Reports/{localID}.json', 'w') as f:
                json_object = json.dumps(r, indent=4)
                f.write(json_object)
        elif domain == "aomedia.googlesource.com":
            if link[-1]=='':
                continue
            link[-1] = link[-1] + "%5E%21/"
            fix_link = '/'.join(link)
            r['fix'] = fix_link
            with open(f'./Reports/{localID}.json', 'w') as f:
                json_object = json.dumps(r, indent=4)
                f.write(json_object)
        elif domain == "sourceware.org": ### all sourceware.org fixed to github.com
            if link[0] == "https:":
                continue
            link[0] = "https:"                                  # protocol
            link[2] = "github.com"                              # domain recovery
            link[3] = "bminor"                                  # user
            link[4] = "binutils-gdb"                            # project
            try:
                link[5] = "commit"
            except IndexError as e:
                link.append("commit")
                link.append(fix_link.split(".git")[1])
            # https://github.com/bminor/binutils-gdb/commit/228c8f4be0c428369ec6b68e25696863d1e62ed7
            # https://sourceware.org/git/?p=binutils-gdb.git;a=commitdiff;h=228c8f4be0c428369ec6b68e25696863d1e62ed7
            fix_link = '/'.join(link)
            r['fix'] = fix_link
            # print(fix_link)
            with open(f'./Reports/{localID}.json', 'w') as f:
                json_object = json.dumps(r, indent=4)
                f.write(json_object) 
        elif domain == "git.sv.nongnu.org":
            # git://git.sv.nongnu.org/freetype/freetype2.git/commits/e9a154e70015e602d695d65a588ecb38f5bb38cc
            # https://github.com/Mojang/freetype2/commit/207ca38fb5e99a638e9ea86d86b28fc895661122
            if link[0] == "https:":
                continue
            link[0] = "https:"
            link[2] = "github.com"
            link[3] = "Mojang"
            link[4] = "freetype2"
            try:
                link[5] = "commit"
            except IndexError as e:
                link.append("commit")
                link.append(fix_link.split(".git")[1])
            fix_link = '/'.join(link)
            r['fix'] = fix_link
            # print(fix_link)
            with open(f'./Reports/{localID}.json', 'w') as f:
                json_object = json.dumps(r, indent=4)
                # print(json_object)
                f.write(json_object)
        elif domain == "dawn.googlesource.com":
            if link[-1]=='':
                continue
            link[-1]=link[-1]+"%5E%21/"
            fix_link = '/'.join(link)
            r['fix'] = fix_link
            with open(f'./Reports/{localID}.json', 'w') as f:
                json_object = json.dumps(r, indent=4)
                # print(json_object)
                f.write(json_object)
        elif domain == "anongit.freedesktop.org":
            link[2] = "cgit.freedesktop.org"
            link[-1] = "?id="+link[-1]
            link[-2] = "commit"
            link[-3] = link[-3][:-4]
            del link[3]
            fix_link = '/'.join(link)
            # print(fix_link)
            r['fix'] = fix_link
            with open(f'./Reports/{localID}.json', 'w') as f:
                json_object = json.dumps(r, indent=4)
                f.write(json_object)

if __name__ =="__main__":
    fix_links()
