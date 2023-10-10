from glob import glob
import random
import fx
def get_test_dataset():
    filter1 = "This model's maximum context length"
    fs = glob("./PatchDesc/*")
    res = []
    for fname in fs:
        with open(fname,'r') as f:
            if filter1 not in f.read():
                res.append(int(fname.split("/")[-1][:-4]))
    return res
def random10():
    res = get_test_dataset()
    random.shuffle(res)
    return res[:10]
if __name__ == "__main__":
    # res = random10()
    # print(res)
    RND = [5729, 5498, 13016, 6790, 38900, 28654, 33841, 31535, 32177, 5534]
    fx.XxX(RND[0])