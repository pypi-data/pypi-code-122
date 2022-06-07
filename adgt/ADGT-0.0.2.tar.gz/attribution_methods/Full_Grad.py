from attribution_methods.fullgrad_raw import FullGrad
import torch
class Explainer():
    def __init__(self,model,nclass=1000):
        import copy
        model = copy.deepcopy(model)
        self.model=model
        self.explain=FullGrad(model)


    def get_attribution_map(self,img,target=None):
        if target is None:
            target=torch.argmax(self.model(img),1)
        attributions = self.explain.saliency(img, target_class=target)
        return attributions