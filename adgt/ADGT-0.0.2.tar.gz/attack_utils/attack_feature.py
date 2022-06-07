import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import optim
from torch.autograd import Variable


class FeatureSpaceAttacker():
    def __init__(self, model, batch_size, step_size=0.003, epsilon=0.5/255.*2, perturb_steps=10, distance='l_inf', device=0):
        self.model = model
        self.batch_size = batch_size
        self.step_size = step_size
        self.epsilon = epsilon
        self.perturb_steps = perturb_steps
        self.distance = distance
        self.device = device

    def attack(self, x_natural):
        # define KL-loss
        criterion_kl = nn.KLDivLoss(size_average=False)
        self.model.eval()
        # generate adversarial example
        x_adv = x_natural.detach() + 0.001 * torch.randn(x_natural.shape).cuda(device=self.device).detach()
        if self.distance == 'l_inf':
            for _ in range(self.perturb_steps):
                x_adv.requires_grad_()
                with torch.enable_grad():
                    loss_kl = criterion_kl(F.log_softmax(self.model(x_adv)[1], dim=1),
                                           F.softmax(self.model(x_natural)[1], dim=1))
                grad = torch.autograd.grad(loss_kl, [x_adv])[0]
                x_adv = x_adv.detach() + self.step_size * torch.sign(grad.detach())
                x_adv = torch.min(torch.max(x_adv, x_natural - self.epsilon), x_natural + self.epsilon)
                x_adv = torch.clamp(x_adv, -1.0, 1.0)

        return x_adv