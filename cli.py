# command line interface
from unitTest import *
import sys

if __name__ == "__main__":
    if len(sys.argv)!= 2:
        print("Usage:")
        print("# play with a issue\npython cli.py <issue_numb\
        er>\n# play with a project\npaylon cli.py <project_name>)")
    else:
        para = sys.argv[1]
        if para.isnumeric():
            localId = int(para)
            res = verify(int(para))
            print("+"*0x20)
            print("\t"+str(localId)+":"+str(res))
            print("+"*0x20)
        else:
            queue = find_issues_by_names([para,])
            res = verifyList(queue)
            print("+"*0x20)
            print(queue)
            print(res)
            print("+"*0x20)