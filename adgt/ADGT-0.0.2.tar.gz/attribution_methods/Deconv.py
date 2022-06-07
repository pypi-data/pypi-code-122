import torch
import torch.nn.functional as F
import torch.nn as nn

class Explainer():
    def __init__(self,model,nclass=1000):
        self.model=model
        self.handle = []

        self.activation_maps = []
        self.gbp_results = []

        self.index=[0]

    def reset(self):
        self.activation_maps = []
        self.gbp_results = []
        self.index = [0]

    def get_attribution_map(self,img,target=None,eval=True):
        if eval:
            self.model.eval()

        def forward_hook_fn(module, input, output):
            # 在全局变量中保存 ReLU 层的前向传播输出
            # 用于将来做 guided backpropagation
            self.activation_maps.append(output)


        def backward_hook_fn(module, grad_in, grad_out):
            # ReLU 层反向传播时，用其正向传播的输出作为 guide
            # 反向传播和正向传播相反，先从后面传起
            grad = self.activation_maps[-1-self.index[0]]


            self.index[0] += 1
            gradout = grad_out[0]
            gradout = torch.clamp(gradout, min=0.0)

            # ReLU 正向传播的输出要么大于0，要么等于0，
            # 大于 0 的部分，梯度为1，
            # 等于0的部分，梯度还是 0
            new_grad_in = gradout

            # ReLU 不含 parameter，输入端梯度是一个只有一个元素的 tuple
            return (new_grad_in,)

        for m in self.model.modules():
            if isinstance(m, nn.ReLU) or isinstance(m, nn.LeakyReLU):
                h = m.register_backward_hook(backward_hook_fn)
                self.handle.append(h)
                h = m.register_forward_hook(forward_hook_fn)
                self.handle.append(h)


        #obtain R
        img.requires_grad_(True)
        out = self.model(img)
        if target is None:
            target=torch.argmax(out,1)
        #topk=torch.randint_like(topk,1000)
        iii = torch.LongTensor(range(img.size(0))).cuda()
        temp = torch.autograd.grad(torch.sum(out[iii,target]), img,retain_graph=True)[0]

        for h in self.handle:
            h.remove()

        import gc
        del self.activation_maps,self.gbp_results
        gc.collect()
        return temp.detach()

class Block_Layer(nn.Module):
    def __init__(self,size=1):
        super(Block_Layer,self).__init__()
        self.relu=nn.ReLU()
        self.size=size
    def forward(self,x):
        mask = torch.ones_like(x)
        s = int(self.size * x.size(2) / 7)
        mask[:, :, :s, :s] = 0
        x = self.relu(x*mask)
        return x
