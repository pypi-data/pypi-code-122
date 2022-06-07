import numpy as np
import torch
from torch.autograd import Variable
import torch.nn.functional as F
class Explainer():
    def __init__(self, model, layer=None,nclass=1000):
        self.model = model
        self.model.eval()
        if layer is None:
            if hasattr(model,'conv4_x'):
                layer='conv4_x'
            elif hasattr(model,'layer4'):
                layer='layer4'
            elif hasattr(model,'layer3'):
                layer='layer3'
            elif hasattr(model,'features'):
                if hasattr(model.features,'51'):
                    layer='features.51'
                elif hasattr(model.features,'42'):
                    layer = 'features.42'#'features.29'
                else:
                    layer = 'features.26'
            elif hasattr(model,'main'):
                if hasattr(model.main,'46'):
                    layer='main.37'
                elif hasattr(model.main,'37'):
                    layer = 'main.28'
                elif hasattr(model.main,'28'):
                    layer = 'main.19'
                else:
                    layer='main.10'
        self.explainer = GradCam(model=model, target_layer_names=layer)

    def get_attribution_map(self, img, target=None):
        attributions = self.explainer(img, target)
        return attributions

class FeatureExtractor:
    """ Class for extracting activations and
    registering gradients from targeted intermediate layers """
    def __init__(self, model, target_layers):
        self.model = model
        self.target_layers = target_layers
        self.gradients = []
        self.hooks=[]
        self.X=0

    def _backward_hook(self, module, grad_input, grad_output, ):
        self.gradients.append(grad_input[0])

    def _forward_hook(self,module, input, output):
        self.X=output
    def get_module(self):
        temp = self.target_layers.split('.')
        #print(temp[0])
        if len(temp) == 1:
            return(self.model.__getattr__(temp[0]))
        else:
            return(self.model.__getattr__(temp[0]).__getattr__(temp[1]))

    def __call__(self, x,target):
        t=self.get_module()
        h1=t.register_forward_hook(self._forward_hook)
        self.hooks.append(h1)
        h2=t.register_backward_hook(self._backward_hook)
        self.hooks.append(h2)
        outputs=self.model(x)
        #one_hot=torch.zeros_like(outputs)
        #for i in range(one_hot.size(0)):
        #    one_hot[i,target[i]]=1
        #temp=torch.sum(outputs*one_hot)
        iii= torch.LongTensor(range(outputs.size(0))).cuda()
        temp=torch.sum(outputs[iii,target])
        temp.backward()
        #input_gradients = torch.autograd.grad(outputs=temp, inputs=x)[0]
        return outputs, self.X,self.gradients[0]
class ModelOutputs:
    """ Class for making a forward pass, and getting:
    1. The network output.
    2. Activations from intermediate targeted layers.
    3. Gradients from intermediate targeted layers. """
    def __init__(self, model, target_layers):
        self.model = model
        self.feature_extractor = FeatureExtractor(self.model, target_layers)

    def get_gradients(self):
        # Retrieve the saved gradients for the target layer
        return self.feature_extractor.gradients

    def __call__(self, x,target):
        output,mid,grad=self.feature_extractor(x,target)
        for h in self.feature_extractor.hooks:
            h.remove()
        self.feature_extractor.hooks=[]
        self.feature_extractor.gradients=[]
        self.feature_extractor.X=0
        return output,mid,grad
class GradCam:
    """
    This class computes the Grad-CAM mask for the specified index.
    """
    def __init__(self, model, target_layer_names):
        self.model = model
        self.model.eval()
        self.extractor = ModelOutputs(self.model, target_layer_names)

    def __call__(self, image_tensor, label=None):
        if label is None:
            output = self.model(image_tensor)
            label = torch.topk(output, 1)
        self.model.zero_grad()
        output,features,grad  = self.extractor(image_tensor,label)

        #print(features,grad)
        weights = torch.mean(torch.mean(grad, dim=3,keepdim=True), dim=2,keepdim=True)

        #target = features[-1]
        #print(grads_val.size(),target.size())
        cam=F.relu(torch.sum(weights*features,dim=1,keepdim=True))
        cam=F.interpolate(cam, size=(image_tensor.size(2), image_tensor.size(3)), mode='bilinear', align_corners=True)

        return cam