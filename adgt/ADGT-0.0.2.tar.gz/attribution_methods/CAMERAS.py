from .CAMERAS_raw import CAMERAS

import torch
import torch.nn.functional as F
class Explainer():
    def __init__(self,model,nclass=1000):
        self.model=model
        name='features'
        if hasattr(model,'layer4'):
            name='layer4'
        elif hasattr(model,'layer3'):
            name='layer3'
        self.explain=CAMERAS(model,targetLayerName=name)
        self.model.eval()

    def get_attribution_map(self,img,target=None):
        if target is None:
            target=torch.argmax(self.model(img),1)
        attributions = self.explain.attribute(img, target=target)
        return F.relu(attributions)
