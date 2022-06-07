from attribution_methods.fullgrad import FullGrad
import torch
class Explainer():
    def __init__(self,model,no_grad=True,nclass=1000):
        self.model=model
        self.explain=FullGrad(model,no_grad)


    def get_attribution_map(self,img,target=None):
        if target is None:
            target=torch.argmax(self.model(img),1)
        attributions = self.explain.attribute(img, target=target)
        return attributions

    def get_condition(self,img):
        condition=self.explain.get_condition(img)
        return condition