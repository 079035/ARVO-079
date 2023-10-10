from OpenAI_gpt import GPT,GPTfix
from pathlib import Path
from Diff import getDiff
REPORTS_DIR = Path("./Reports")
def oss_fuzz_get_patch(localID):
    diff_file = getDiff(localID)
    if diff_file == False:
        return False
    with open(diff_file, mode="rb") as f:
        content = f.read()
        try:
            return content.decode()
        except UnicodeDecodeError as e:
            return content.decode('latin-1')
    
def oss_fuzz_vul_labeler(localID):
    print(f"[+] Labeling case {localID}...")
    diff = oss_fuzz_get_patch(localID)
    if diff == False:
        return False
    ins = GPT()
    res = ins.api_call(f"Can you describe what vulnerability could be patched in following diff file?\nDiff information:\n```\n{diff}\n```")
    return res
if __name__ == "__main__":
    res = oss_fuzz_vul_labeler(31585)
    print(res)