from captum.attr import DeepLift

import torch
import torch.nn.functional as F

class Explainer():
    def __init__(self,model,nclass=1000):
        self.model=model
        self.model.eval()
        self.explain=DeepLift(model)


    def get_attribution_map(self,img,target=None):
        if target is None:
            target=torch.argmax(self.model(img),1)
        if len(img.size()) > 2 and img.size(2) >= 224:
            thrd = 2
        else:
            thrd = 20
        baseline_dist = torch.randn_like(img) * 0.001
        #attributions, delta = self.explain.attribute(img, baseline_dist, target=target, return_convergence_delta=True)

        attributions = []
        if img.size(0) > thrd:
            img = torch.split(img, thrd)
            target = torch.split(target, thrd)
            baseline_dist = torch.split(baseline_dist, thrd)
        else:
            img, target, baseline_dist = [img], [target], [baseline_dist]

        for i, t, b in zip(img, target, baseline_dist):
            temp = self.explain.attribute(i, b, target=t, return_convergence_delta=False)
            attributions.append(temp)

        attributions = torch.cat(tuple(attributions), 0)
        #return F.relu(attributions)
        return attributions