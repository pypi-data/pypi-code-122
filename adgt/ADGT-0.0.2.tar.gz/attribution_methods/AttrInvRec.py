from attribution_methods.air import AIR
import torch

class Explainer():
    def __init__(self,model):
        self.model=model
        self.explain=AIR(model)


    def get_attribution_map(self,img,target=None,module_name='fc',max_k=50):
        if target is None:
            target=torch.argmax(self.model(img),1)
        attributions = self.explain.attribute(img, target=target,module_name=module_name,max_k=max_k)
        return attributions