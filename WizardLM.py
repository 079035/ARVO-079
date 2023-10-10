from Locator import *
import _profile
import json
import requests
API_URL = "https://api-inference.huggingface.co/models/WizardLM/WizardCoder-15B-V1.0"
# API_URL = "https://huggingface.co/inference-endpoints"
headers = {"Authorization": f"Bearer {_profile.HF_TOKEN}"}

class Wizard():    
    def __init__(self,src_path):
        self.api_key = _profile.HF_TOKEN
        self.src = src_path
    
    def fixer(self,code,ins="Fix the potential vulnerability",n=1,temperature=0):
        payload={
        "input": code,
        "instruction": ins,
        }
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))

# Raw requests
def run(code,ins="Fix potential vulnerabilities",n=1,temperature=0):
    case = Wizard(".")
    return_code = case.fixer(code,ins=ins,n=n,temperature=temperature)
    return return_code


if __name__ == "__main__":
    test_code='''
    #include<stdio.h>
    int main(){
        char buf[0x1000];
        read(stdin,buf,0x10000);
    }
    '''
    res = run(test_code,n=5,temperature=1)
    print(res)