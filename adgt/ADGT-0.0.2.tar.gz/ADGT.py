import torchvision.transforms as transforms
from utils.visualization import save_images,save_images3
import torch
import torch.nn as nn
import torch.nn.functional as F
import os
import numpy as np

class ADGT():
    nclass={'MNIST':10,'C10':10,'C100':100,'Flower102':102,'RestrictedImageNet':9,'ImageNet':1000}

    def __init__(self,name='MNIST',nclass=None,use_cuda=True):
        self.use_cuda=use_cuda
        self.dataset_name=name
        if nclass is not None:
            self.nclass[name]=nclass

    def obtain_statistics(self):
        K=self.nclass[self.dataset_name]
        mu=None
        X2=None
        num = None  # numbers of samples except class
        mu_in=None
        X2_in=None
        num_in=None
        print('obtain statistics')
        for data, label in self.trainloader:
            C,H,W=data.size(1),data.size(2),data.size(3)
            self.channels,self.heights,self.width=C,H,W
            data_temp = data.permute([1, 0, 2, 3])
            data_temp = data_temp.reshape(C, -1)
            if self.min is None:
                self.min=torch.min(data_temp,1)[0].view(1,-1,1,1)
                self.max=torch.max(data_temp,1)[0].view(1,-1,1,1)
            else:
                m1=torch.cat([data_temp,self.min.view(-1,1)],1)
                m2=torch.cat([data_temp,self.max.view(-1,1)],1)
                self.min = torch.min(m1, 1)[0].view(1, -1, 1, 1)
                self.max = torch.max(m2, 1)[0].view(1, -1, 1, 1)

            if mu is None:
                mu=torch.zeros(K,C,H,W)
                X2=torch.zeros(K,C,H,W)
                num=torch.zeros(K,1,1,1)
                mu_in=torch.zeros(K,C,H,W)
                X2_in = torch.zeros(K, C, H, W)
                num_in = torch.zeros(K, 1, 1, 1)

            for i in range(K):
                temp=data[label!=i]
                mu[i]=mu[i]+torch.sum(temp,0,keepdim=True)
                X2[i]=X2[i]+torch.sum(temp**2,0,keepdim=True)
                num[i]+=temp.size(0)

                temp_in = data[label == i]
                if temp_in.size(0)>0:
                    mu_in[i] = mu[i] + torch.sum(temp_in, 0, keepdim=True)
                    X2_in[i] = X2[i] + torch.sum(temp_in ** 2, 0, keepdim=True)
                    num_in[i] += temp_in.size(0)

        self.mu=mu/num
        X2=X2/num
        self.var=X2-self.mu**2

        self.mu_in = mu_in / num_in
        X2_in = X2_in / num_in
        self.var_in = X2_in - self.mu_in ** 2

        print('min:',self.min,'max:',self.max)
        print('mean:',self.mu)
        print('var:',self.var)

        self.right_prob = torch.zeros(K, C, H, W, 2)
        epsilon=1e-4
        for data, label in self.trainloader:
            for i in range(K):
                temp_in = data[label == i]
                if temp_in.size(0) > 0:
                    temp_min=torch.sign(F.relu(self.min-temp_in+epsilon))
                    temp_max=torch.sign(F.relu(temp_in+epsilon-self.max))
                    self.right_prob[i,:,:,:,0]+=torch.sum(temp_min,0)
                    self.right_prob[i, :, :, :, 1] += torch.sum(temp_max, 0)
        self.right_prob=self.right_prob/num_in.view(K,1,1,1,1)
    def pure_explain(self,img,model,method,file_name=None,color=False,suffix='', grad=False,target=None,k=3):
        if target is None:
            pred=model(img)
            target=torch.argmax(pred,1)
        def obtain_explain(alg,target=target):
            obj = alg.Explainer(model,nclass=self.nclass[self.dataset_name])
            if method=='TRGBP':
                mask = obj.get_attribution_map(img, target,k)
            else:
                mask = obj.get_attribution_map(img, target)
            return mask
        if method=='GradientSHAP':
            from attribution_methods import GradientSHAP
            mask=obtain_explain(GradientSHAP)
        elif method=='DeepLIFTSHAP':
            from attribution_methods import DeepLIFTSHAP
            mask=obtain_explain(DeepLIFTSHAP)
        elif method=='Guided_BackProp':
            from attribution_methods import Guided_BackProp
            mask=obtain_explain(Guided_BackProp)
        elif method=='DeepLIFT':
            from attribution_methods import DeepLIFT
            mask=obtain_explain(DeepLIFT)
        elif method=='IntegratedGradients':
            from attribution_methods import IntegratedGradients
            mask=obtain_explain(IntegratedGradients)
        elif method=='InputXGradient':
            from attribution_methods import InputXGradient
            mask=obtain_explain(InputXGradient)
        elif method == 'Occlusion':
            from attribution_methods import Occlusion
            mask = obtain_explain(Occlusion)
        elif method == 'Saliency':
            from attribution_methods import Saliency
            mask = obtain_explain(Saliency)
        elif method=='GradCAM':
            from attribution_methods import Grad_CAM,Grad_CAM_batch
            mask= obtain_explain(Grad_CAM)
            #mask, mask_random = obtain_explain(Grad_CAM_batch, random)
        elif method=='SmoothGrad':
            from attribution_methods import SmoothGrad
            mask = obtain_explain(SmoothGrad)
        elif method=='RectGrad':
            from attribution_methods import RectGrad
            mask = obtain_explain(RectGrad)
        elif method=='FullGrad':
            from attribution_methods import Full_Grad
            mask = obtain_explain(Full_Grad)
        elif method=='random':
            return torch.mean(torch.rand_like(img),1,keepdim=True)
        elif method=='CAMERAS':
            from attribution_methods import CAMERAS
            mask = obtain_explain(CAMERAS)
        elif method == 'GIG':
            from attribution_methods import GIG
            mask = obtain_explain(GIG)
        elif method=='TRGBP':
            from attribution_methods import TRGBP
            mask=obtain_explain(TRGBP)
        elif method=='Deconv':
            from attribution_methods import Deconv
            mask=obtain_explain(Deconv)
        elif method=='LRP':
            from attribution_methods import LRP
            mask=obtain_explain(LRP)
        else:
            print(method)
            print('no this method')
        if file_name is not None:
            if not os.path.exists(file_name):
                os.mkdir(file_name)
            if method!='TRGBP':
                temp=mask.detach().cpu().numpy()
                save_images3(temp, os.path.join(file_name, method+suffix+'.png'))
            else:
                #TRGBP_M,TRGBP_R, TRGBP_K=mask
                TRGBP_M = mask
                for i in range(len(TRGBP_M)):
                    save_images3(TRGBP_M[i].detach().cpu().numpy(), os.path.join(file_name, str(i) + '_TRGBP-M'+suffix + '.png'))
        if not grad and method!='TRGBP':
            mask=mask.detach()
        return mask
    def standardize(self,X):
        minn = np.min(X.reshape([X.shape[0], -1]), axis=1)
        maxx = np.max(X.reshape([X.shape[0], -1]), axis=1)
        if X.ndim == 4:
            minn = minn.reshape([X.shape[0], 1, 1, 1])
            maxx = maxx.reshape([X.shape[0], 1, 1, 1])
        elif X.ndim == 3:
            minn = minn.reshape([X.shape[0], 1, 1])
            maxx = maxx.reshape([X.shape[0], 1, 1])
        else:
            minn = minn.reshape([X.shape[0], 1])
            maxx = maxx.reshape([X.shape[0], 1])

        X = (X - minn) / (maxx - minn + 1e-8)
        return X
    def fft(self,img,logdir=None):
        import scipy.fftpack as fp
        img = self.standardize(img)
        #img = np.mean(img, axis=1)
        ## Functions to go from image to frequency-image and back
        im2freq = lambda data: fp.fft(fp.fft(data, axis=2),
                                       axis=3)
        freq2im = lambda f: fp.ifft(fp.ifft(f, axis=2),
                                     axis=3)
        #f = im2freq(img)

        f=np.fft.fftn(img,axes=(-2,-1))

        f_mag = np.fft.fftshift(f,axes=(-2,-1))
        f_mag=np.abs(f_mag)


        if logdir is not None:
            if not os.path.exists(logdir):  # 如果路径不存在
                os.makedirs(logdir)
            save_images(img, os.path.join(logdir, 'raw.png'))
            save_images(np.log(1+f_mag), os.path.join(logdir, 'f_mag.png'))
        return f



