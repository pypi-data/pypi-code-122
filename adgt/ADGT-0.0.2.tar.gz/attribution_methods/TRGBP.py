import torch
import torch.nn.functional as F
import torch.nn as nn

def norm(go):
    return go
def norm_l2(go):
    temp=go
    go = go.view(go.size(0), -1)
    a = torch.sqrt(torch.sum(go * go, 1, keepdim=True))
    # a=1
    go = go / (a + 1e-8)
    go = go.view_as(temp)
    return go
def norm_max(go):
    temp=go
    go = go.view(go.size(0), -1)
    #a = torch.sqrt(torch.sum(go * go, 1, keepdim=True))
    a,_ = torch.max(go, 1, keepdim=True)
    # a=1
    go = go / (a + 1e-8)
    go = go.view_as(temp)
    return go
class Explainer_k():
    def __init__(self,model,nclass=1000,bias=False):
        self.model=model
        self.handle = []

        self.activation_maps = []
        self.gbp_results = []
        self.bias_term=[]
        self.bias=bias
        self.index=[0]

    def reset(self):
        self.activation_maps = []
        self.gbp_results = []
        self.bias_term = []
        self.index = [0]

    def get_attribution_map(self,img,target=None,k=3,eval=True):
        if eval:
            self.model.eval()

        def forward_hook_fn(module, input, output):
            # 在全局变量中保存 ReLU 层的前向传播输出
            # 用于将来做 guided backpropagation
            self.activation_maps.append(output)
        def forward_bias_hook_fn(module,input,output):
            self.bias_term.append(module.bias.data)

        def backward_hook_fn(module, grad_in, grad_out):
            # ReLU 层反向传播时，用其正向传播的输出作为 guide
            # 反向传播和正向传播相反，先从后面传起
            grad = self.activation_maps[-1-self.index[0]]

            go=grad_out[0]*grad
            if self.bias:
                bias = self.bias_term[-2 - self.index[0]]
                if len(go.size())==4:
                    go=go*bias.view(1, -1, 1, 1)
            self.index[0] += 1
            if len(go.size())==4:
                go=norm(go)#*grad
                self.gbp_results.append(go.detach())
            gradout = grad_out[0]
            gradout = torch.clamp(gradout, min=0.0)

            # ReLU 正向传播的输出要么大于0，要么等于0，
            # 大于 0 的部分，梯度为1，
            # 等于0的部分，梯度还是 0
            new_grad_in = gradout * torch.sign(grad)

            # ReLU 不含 parameter，输入端梯度是一个只有一个元素的 tuple
            return (new_grad_in,)

        for m in self.model.modules():
            if isinstance(m, nn.ReLU) or isinstance(m, nn.LeakyReLU):
                h = m.register_backward_hook(backward_hook_fn)
                self.handle.append(h)
                h = m.register_forward_hook(forward_hook_fn)
                self.handle.append(h)
            elif isinstance(m, nn.Conv2d) or isinstance(m, nn.Linear):
                if self.bias:
                    h = m.register_forward_hook(forward_bias_hook_fn)
                    self.handle.append(h)


        #obtain R
        img.requires_grad_(True)
        out = self.model(img)
        if target is None:
            target=torch.argmax(out,1)
        _,topk=torch.topk(out,k,1)
        #topk=torch.randint_like(topk,1000)
        iii = torch.LongTensor(range(img.size(0))).cuda()
        temp = torch.autograd.grad(torch.sum(out[iii,target]), img,retain_graph=True)[0]
        self.gbp_results.append(norm(temp.detach()*img.detach()))
        R_temp=self.gbp_results

        #obtain K and M
        rg=True
        K_temp=[]
        M_temp=[]
        for i in range(k):
            self.gbp_results=[]
            self.index=[0]
            if i==k-1:
                rg=False
            temp = torch.autograd.grad(torch.sum(out[iii, topk[:,i]]), img, retain_graph=rg)[0]
            #temp = torch.autograd.grad(torch.sum(out*norm(torch.randn_like(out))), img, retain_graph=rg)[0]
            self.gbp_results.append(norm(temp.detach()*img.detach()))
            K_temp.append(self.gbp_results)
            if len(M_temp)==0:
                for j in range(len(self.gbp_results)):
                    M_temp.append(self.gbp_results[j]/k)
            else:
                for j in range(len(self.gbp_results)):
                    M_temp[j]+=self.gbp_results[j]/k

        M=M_temp
        R=[]
        K=[]
        for i in range(len(R_temp)):
            R.append(R_temp[i]-M[i])
            K.append([])
            for j in range(k):
                K[i].append(K_temp[j][i]-M[i])

        for h in self.handle:
            h.remove()

        import gc
        del self.activation_maps,self.gbp_results
        gc.collect()
        return M,R,K

class Explainer():
    def __init__(self,model,nclass=1000,bias=False):
        self.model=model
        self.handle = []

        self.activation_maps = []
        self.gbp_results = []
        self.bias_term=[]
        self.bias=bias
        self.index=[0]

    def reset(self):
        self.activation_maps = []
        self.gbp_results = []
        self.bias_term = []
        self.index = [0]

    def get_attribution_map(self,img,target=None,k=3,eval=True):
        if eval:
            self.model.eval()

        def forward_hook_fn(module, input, output):
            # 在全局变量中保存 ReLU 层的前向传播输出
            # 用于将来做 guided backpropagation
            self.activation_maps.append(output)
        def forward_bias_hook_fn(module,input,output):
            self.bias_term.append(module.bias.data)

        def backward_hook_fn(module, grad_in, grad_out):
            # ReLU 层反向传播时，用其正向传播的输出作为 guide
            # 反向传播和正向传播相反，先从后面传起
            grad = self.activation_maps[-1-self.index[0]]

            go=grad_out[0]*grad
            if self.bias:
                bias = self.bias_term[-2 - self.index[0]]
                if len(go.size())==4:
                    go=go*bias.view(1, -1, 1, 1)
            self.index[0] += 1
            if len(go.size())==4:
                #go=norm(go)#*grad
                self.gbp_results.append(go.detach())
            gradout = grad_out[0]
            gradout = torch.clamp(gradout, min=0.0)

            # ReLU 正向传播的输出要么大于0，要么等于0，
            # 大于 0 的部分，梯度为1，
            # 等于0的部分，梯度还是 0
            new_grad_in = gradout * torch.sign(grad)

            # ReLU 不含 parameter，输入端梯度是一个只有一个元素的 tuple
            return (new_grad_in,)

        for m in self.model.modules():
            if isinstance(m, nn.ReLU) or isinstance(m, nn.LeakyReLU):
                h = m.register_backward_hook(backward_hook_fn)
                self.handle.append(h)
                h = m.register_forward_hook(forward_hook_fn)
                self.handle.append(h)
            elif isinstance(m, nn.Conv2d) or isinstance(m, nn.Linear):
                if self.bias:
                    h = m.register_forward_hook(forward_bias_hook_fn)
                    self.handle.append(h)


        #obtain R
        img.requires_grad_(True)
        out = self.model(img)
        if target is None:
            target=torch.argmax(out,1)
        _,topk=torch.topk(out,k,1)
        #print(topk)
        #topk=torch.randint_like(topk,1000)
        iii = torch.LongTensor(range(img.size(0))).cuda()
        temp = torch.autograd.grad(torch.sum(out[iii,target]), img,retain_graph=True)[0]
        self.gbp_results.append(temp.detach()*img.detach())
        R_temp=self.gbp_results

        #obtain K and

        for h in self.handle:
            h.remove()

        import gc
        del self.activation_maps,self.gbp_results
        gc.collect()
        return R_temp

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
