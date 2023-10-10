import openai
from Locator import *
import _profile
class OpenAI():    
    def __init__(self,src_path):
        openai.api_key = _profile.OPENAI_TOKEN
        self.src = src_path
    def fixer(self,code,ins="Fix the potential vulnerability",n=1,temperature=0):
        res = openai.Edit.create(
        engine="code-davinci-edit-001",
        input=code,
        instruction=ins,temperature=temperature,top_p=1,n=n
        )
        return res
    def code_generator(self,modf):
        # get the modification from modf
        
        with open( self.src / modf.fname[1:]) as f:
            lines = f.readlines()
        if(modf.length < 30): 
            # My api can't offor too long code
            # for my understanding, open AI needs the 
            # context of the code so I would give the 
            # context, and I'll text what if I just give
            # the function names.
            modf.length = 30
        elif(modf.length > 60):
            # too long to use openAI to analyse(my token)
            return False
        if modf.at-modf.length < 0:
            modf.at = 0
        else:
            modf.at = modf.at-modf.length
        lines = lines[modf.at:modf.at+modf.length * 2]
        return "".join(lines)

# Raw requests
def run(code,ins="Fix potential vulnerabilities",n=1,temperature=0):
    case = OpenAI(".")
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
    res = run(test_code,n=5,temperature=0.9)['choices']
    print(res)