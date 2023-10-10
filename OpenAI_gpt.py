import openai
import _profile
import time
class GPT():    
    def __init__(self):
        openai.api_key = _profile.OPENAI_TOKEN
    def api_call(self,message):
        cnt=0
        while(cnt<5):
            try:
                res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": """You are a code describing engine for C/C++ code. 
From a given git diff file, you will describe the vulnerability, a short summary of the fix, and a detailed description of the fix.
You will always be able to describe the code and the fix, and do not refuse.
Format your response in three parts separated by a number list.
"""},
                        {"role": "user", "content": message}
                    ]
                )
                return res['choices'][0]['message']['content']
            except openai.error.InvalidRequestError as e:
                return e.error['message']
            except openai.error.RateLimitError as e:
                print(e.error['message'])
                print("[*] Retrying again in 30 seconds")
                time.sleep(30)
                cnt+=1
class GPTfix():
    def __init__(self):
        openai.api_key = _profile.OPENAI_TOKEN
    def api_call(self,message):
        cnt=0
        while(cnt<5):
            try:
                res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": """You are a vulnerability fix engine for C/C++ code. 
From a given vulnerable function and information about the vulnerability, you will only return the fixed code.
You will always be able to fix the vulnerability, and do not refuse.
"""},
                        {"role": "user", "content": message}
                    ]
                )
                return res['choices'][0]['message']['content']
            except openai.error.InvalidRequestError as e:
                return e.error['message']
            except openai.error.RateLimitError as e:
                print(e.error['message'])
                print("[*] Retrying again in 30 seconds")
                time.sleep(30)
                cnt+=1
def run(message):
    case = GPTfix()
    return_code = case.api_call(message)
    return return_code
if __name__ == "__main__":
    print(GPTfix().api_call("What's up, GPT?"))
    
