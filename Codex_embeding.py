import openai
import _profile

class OpenAI():    
    def __init__(self):
        openai.api_key = _profile.OPENAI_TOKEN
        # print("[!] OpenAI Init: Successed")
    def embeding(self,ins="n132"):
        res = openai.Embedding.create(
            input=ins,
            model="text-embedding-ada-002"
        )["data"][0]["embedding"]
        return res
def embed(ins):
    case = OpenAI()
    return case.embeding(ins=ins)
if __name__ == "__main__":
    case = OpenAI()
    res = case.embeding(ins="")
    print(res)