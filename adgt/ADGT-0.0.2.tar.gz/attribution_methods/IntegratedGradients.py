from captum.attr import IntegratedGradients

import torch
import torch.nn.functional as F
class Explainer():
    def __init__(self,model,nclass=1000):
        self.model=model
        self.explain=IntegratedGradients(model)
        self.model.eval()


    def get_attribution_map(self,img,target=None):
        if target is None:
            target=torch.argmax(self.model(img),1)
        baseline_dist = torch.randn_like(img) * 0.001
        if len(img.size())>2 and img.size(2)>=224:
            thrd=2
        else:
            thrd=16
        attributions=[]
        if img.size(0) > thrd:
            img=torch.split(img,thrd)
            target=torch.split(target,thrd)
            baseline_dist=torch.split(baseline_dist,thrd)
        else:
            img,target,baseline_dist=[img],[target],[baseline_dist]

        for i,t,b in zip(img,target,baseline_dist):
            temp = self.explain.attribute(i, b, target=t , return_convergence_delta=False,n_steps=10)
            attributions.append(temp)

        attributions=torch.cat(tuple(attributions),0)
        #return torch.abs(attributions)
        return attributions