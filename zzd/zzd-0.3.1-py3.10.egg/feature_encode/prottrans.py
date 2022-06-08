import numpy as np
import os

class prottrans:
    def __init__(self,prottrans_file=f"{os.environ['HOME']}/.local/zzd/lib/prottrans_embs.pkl"):
        self.prottrans = None
        self.prottrans_file = prottrans_file
    
    def __getitem__(self,index):
        if self.prottrans == None:
            self.prottrans = np.load(self.prottrans_file, allow_pickle=True)
        return self.prottrans[index]

if __name__ == "__main__":
    test = prottrans()['AT3G17090']
    print(test,test.shape)
