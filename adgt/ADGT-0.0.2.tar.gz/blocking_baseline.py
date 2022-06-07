import argparse
import os
import random
import shutil
import time
import warnings
import json
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.optim
import torch.multiprocessing as mp
import torch.utils.data
import torch.utils.data.distributed
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models
from torch.utils.tensorboard import SummaryWriter
from model import resnet,vgg
import numpy as np
import torch.nn.functional as F
import matplotlib.pyplot as plt
from utils.visualization import save_images,save_images2

DATASET='test'#'train'#
ROOT='result'
if not os.path.exists(ROOT):
    os.mkdir(ROOT)
method=['DeepLIFT','IntegratedGradients','InputXGradient','GradCAM','FullGrad','CAMERAS','LRP','Deconv','Guided_BackProp']

SIZE=3
POSITION=12#7#2#-1#

torch.set_num_threads(4)
os.environ["CUDA_VISIBLE_DEVICES"] = "7"

def setup_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)

model_names = sorted(name for name in models.__dict__
    if name.islower() and not name.startswith("__")
    and callable(models.__dict__[name]))

parser = argparse.ArgumentParser(description='PyTorch ImageNet Training')
parser.add_argument('--data', metavar='DIR',default='/data_SSD2/zgh/workspace/data/ImageNet',
                    help='path to dataset')
parser.add_argument('-a', '--arch', metavar='ARCH', default='resnet50',
                    choices=model_names,
                    help='model architecture: ' +
                        ' | '.join(model_names) +
                        ' (default: resnet18)')
parser.add_argument('-j', '--workers', default=4, type=int, metavar='N',
                    help='number of data loading workers (default: 4)')
parser.add_argument('--epochs', default=90, type=int, metavar='N',
                    help='number of total epochs to run')
parser.add_argument('--start-epoch', default=0, type=int, metavar='N',
                    help='manual epoch number (useful on restarts)')
parser.add_argument('-b', '--batch-size', default=16, type=int,
                    metavar='N',
                    help='mini-batch size (default: 256), this is the total '
                         'batch size of all GPUs on the current node when '
                         'using Data Parallel or Distributed Data Parallel')
parser.add_argument('--lr', '--learning-rate', default=0.1, type=float,
                    metavar='LR', help='initial learning rate', dest='lr')
parser.add_argument('--momentum', default=0.9, type=float, metavar='M',
                    help='momentum')
parser.add_argument('--wd', '--weight-decay', default=1e-4, type=float,
                    metavar='W', help='weight decay (default: 1e-4)',
                    dest='weight_decay')
parser.add_argument('-p', '--print-freq', default=10, type=int,
                    metavar='N', help='print frequency (default: 10)')
parser.add_argument('--resume', default='', type=str, metavar='PATH',
                    help='path to latest checkpoint (default: none)')
parser.add_argument('-e', '--evaluate', dest='evaluate', action='store_true',
                    help='evaluate model on validation set')
parser.add_argument('--pretrained', dest='pretrained', action='store_true',
                    help='use pre-trained model')
parser.add_argument('--world-size', default=-1, type=int,
                    help='number of nodes for distributed training')
parser.add_argument('--rank', default=-1, type=int,
                    help='node rank for distributed training')
parser.add_argument('--dist-url', default='tcp://224.66.41.62:23456', type=str,
                    help='url used to set up distributed training')
parser.add_argument('--dist-backend', default='nccl', type=str,
                    help='distributed backend')
parser.add_argument('--seed', default=None, type=int,
                    help='seed for initializing training. ')
parser.add_argument('--gpu', default=None, type=int,
                    help='GPU id to use.')
parser.add_argument('--multiprocessing-distributed', action='store_true',
                    help='Use multi-processing distributed training to launch '
                         'N processes per node, which has N GPUs. This is the '
                         'fastest way to use PyTorch for either single node or '
                         'multi node data parallel training')



def main():
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)
        torch.manual_seed(args.seed)
        cudnn.deterministic = True
        warnings.warn('You have chosen to seed training. '
                      'This will turn on the CUDNN deterministic setting, '
                      'which can slow down your training considerably! '
                      'You may see unexpected behavior when restarting '
                      'from checkpoints.')

    if args.gpu is not None:
        warnings.warn('You have chosen a specific GPU. This will completely '
                      'disable data parallelism.')

    if args.dist_url == "env://" and args.world_size == -1:
        args.world_size = int(os.environ["WORLD_SIZE"])

    args.distributed = args.world_size > 1 or args.multiprocessing_distributed

    ngpus_per_node = torch.cuda.device_count()

    cudnn.benchmark = True

    traindir = os.path.join(args.data, 'train')
    valdir = os.path.join(args.data, 'val')
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])
    '''
    train_dataset = datasets.ImageFolder(
        traindir,
        transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            normalize,
        ]))
    if args.distributed:
        train_sampler = torch.utils.data.distributed.DistributedSampler(train_dataset)
    else:
        train_sampler = None
    train_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=args.batch_size, shuffle=(train_sampler is None),
        num_workers=args.workers, pin_memory=True, sampler=train_sampler)
    '''
    setup_seed(999)
    val_loader = torch.utils.data.DataLoader(
        datasets.ImageFolder(valdir, transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            normalize,
        ])),
        batch_size=args.batch_size, shuffle=True,
        num_workers=args.workers, pin_memory=False)

    main_worker(val_loader,POSITION,SIZE, args)

from attribution_methods.TRGBP import Block_Layer

def blocking_model(model,target_layer=2,size=1):
    print(len(model.features))
    index=-1
    for i in range(len(model.features)):
        if isinstance(model.features[i], nn.ReLU):
            index+=1
            if index + target_layer == 12:
                model.features[i]=Block_Layer(size)
    return model

def energy_rate(x,size=1):
    mask=torch.zeros_like(x)
    s=int(size*x.size(2)/7)
    mask[:,:,:s,:s]=1
    x=torch.abs(x)
    er=torch.sum(x*mask)/(torch.sum(x))
    return er.item()

def main_worker(val_loader,position,size, args):
    # create model
    model=vgg.vgg16(pretrained=True).cuda()
    if position>=0:
        model=blocking_model(model,position,size)
    model.eval()
    import ADGT
    adgt = ADGT.ADGT(use_cuda=True, name='ImageNet')
    if DATASET=='train':
        loader=None
    else:
        loader=val_loader
    pth = os.path.join(ROOT, 'Blocking_baseline',str(position)+'_'+str(size))
    if not os.path.exists(os.path.join(ROOT, 'Blocking_baseline')):
        os.mkdir(os.path.join(ROOT, 'Blocking_baseline'))
    if not os.path.exists(pth):
        os.mkdir(pth)
    if True:
        end = time.time()
        result = {}
        for i, (images, target) in enumerate(loader):
            images, target = images.cuda(), target.cuda()
            if i==0:
                for j in range(images.size(0)):
                    base_img=images[j].unsqueeze(0)
                    print(i,j)
                    for m in method:
                        adgt.pure_explain(base_img, model, m, os.path.join(pth, str(j)+'_VGG'))
                    save_images2(base_img.detach().cpu().numpy(), os.path.join(pth, str(j) + '_VGG', 'raw.png'))
                break
            for m in method:
                print(m)
                mask=adgt.pure_explain(images, model, m)
                er=energy_rate(mask)

                if not m in result:
                    result[m]=er
                else:
                    result[m]=(result[m]*i+er)/(i+1)
            print(i,result)

            np.save(os.path.join(pth, 'baseline.npy'), result)






if __name__ == '__main__':
    main()