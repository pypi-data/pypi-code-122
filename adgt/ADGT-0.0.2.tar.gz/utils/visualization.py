import os
import matplotlib.pyplot as plt
import torch.nn.functional as F
from torchvision import  transforms
plt.switch_backend('agg')
import torch
import torch.nn as nn

def show_cam(raw_img,mask,filename):
    raw_img = raw_img.transpose(0, 2, 3, 1)
    raw_img = raw_img.reshape(raw_img.shape[1], raw_img.shape[2], raw_img.shape[3])
    plt.imshow(raw_img)
    plt.imshow(mask, cmap='jet', alpha=0.5)
    plt.savefig(filename)
    plt.close()
def cut_most(heatmaps,p=1):
    p=100-p
    heatmaps=torch.Tensor(heatmaps).cuda()
    rawgrad = heatmaps
    temp = np.percentile(rawgrad.view(rawgrad.size(0), -1).data.cpu().numpy(), p, axis=1)
    grad = rawgrad

    if len(list(rawgrad.size())) == 4:
        temp = torch.Tensor(temp).cuda().view(rawgrad.size(0), 1, 1, 1)
        # temp2 = torch.Tensor(temp2).cuda().view(grad_out[0].size(0), 1, 1, 1)
    elif len(list(rawgrad.size())) == 3:
        temp = torch.Tensor(temp).cuda().view(rawgrad.size(0), 1,1)
        # temp2 = torch.Tensor(temp2).cuda().view(grad_out[0].size(0), 1)

    return torch.where(torch.le(rawgrad, temp), rawgrad, temp).cpu().numpy()
def cut_least(heatmaps,p=1):
    heatmaps=torch.Tensor(heatmaps).cuda()
    rawgrad = heatmaps
    temp = np.percentile(rawgrad.view(rawgrad.size(0), -1).data.cpu().numpy(), p, axis=1)
    grad = rawgrad

    if len(list(rawgrad.size())) == 4:
        temp = torch.Tensor(temp).cuda().view(rawgrad.size(0), 1, 1, 1)
        # temp2 = torch.Tensor(temp2).cuda().view(grad_out[0].size(0), 1, 1, 1)
    elif len(list(rawgrad.size())) == 3:
        temp = torch.Tensor(temp).cuda().view(rawgrad.size(0), 1,1)
        # temp2 = torch.Tensor(temp2).cuda().view(grad_out[0].size(0), 1)

    return torch.where(torch.ge(rawgrad, temp), rawgrad, temp).cpu().numpy()

def save_images(X, save_path,minn=None,maxx=None,img_num=0,p=1):
    # [0, 1] -> [0,255]
    n_samples = X.shape[0]
    X=np.maximum(X,0)
    #X=cut_most(X,p)
    #X = cut_least(X, p)
    #print(X)
    if True:
        rows = int(np.sqrt(n_samples)) + 1
        while n_samples % rows != 0:
            rows -= 1

        nh, nw = int(rows), int(n_samples / rows)
    else:
        nh=int(img_num)
        nw=int(n_samples/img_num)
    if img_num==0:
        if minn is None:
            minn=np.min(X.reshape([X.shape[0],-1]),axis=1)
            maxx=np.max(X.reshape([X.shape[0],-1]),axis=1)
            if X.ndim == 4:
                minn=minn.reshape([X.shape[0],1,1,1])
                maxx=maxx.reshape([X.shape[0],1,1,1])
            elif X.ndim==3:
                minn = minn.reshape([X.shape[0], 1, 1])
                maxx = maxx.reshape([X.shape[0], 1, 1])
            else :
                minn = minn.reshape([X.shape[0], 1])
                maxx = maxx.reshape([X.shape[0], 1])

            X=(X-minn)/(maxx-minn+1e-8)
        else:
            X = (X - minn) / (maxx - minn + 1e-8)
            X=np.maximum(X,0)
            X=np.minimum(X,1)
    else:
        X_temp=X.reshape([nh,nw,-1])
        minn=np.min(X_temp,axis=0)
        minn=np.min(minn,axis=-1).reshape([1,-1,1,1,1])
        maxx=np.max(X_temp,axis=0)
        maxx=np.max(maxx,axis=-1).reshape([1,-1,1,1,1])
        #print(minn.shape, maxx.shape)
        X_temp = X.reshape([nh, nw, X.shape[1],X.shape[2],X.shape[3]])
        X_temp=(X_temp - minn) / (maxx - minn + 1e-8)
        X=X_temp.reshape(X.shape)
    #X = X.squeeze()
    #if isinstance(X.flatten()[0], np.floating):
    #    #X = (255 * X).astype('uint8')
    #    X=np.uint8(255 * X)



    if X.ndim == 2:
        X = np.reshape(X, (X.shape[0], int(np.sqrt(X.shape[1])), int(np.sqrt(X.shape[1]))))

    if X.ndim == 4:
        # BCHW -> BHWC
        X = X.transpose(0, 2, 3, 1)
        h, w = X[0].shape[:2]
        img = np.zeros((h * nh, w * nw, 3))
    elif X.ndim == 3:
        h, w = X[0].shape[:2]
        img = np.zeros((h * nh, w * nw))

    for n, x in enumerate(X):
        j = int(n / nw)
        i = int(n % nw)
        img[j * h:j * h + h, i * w:i * w + w] = x
    np.set_printoptions(threshold=np.inf)
    #print(save_path,img)
    #plt.imsave(save_path, img)
    #print(img.shape)

    img=np.mean(img,2)
    #img=np.maximum(img,0)

    plt.imshow(img, cmap='jet')
    #plt.imshow(img)
    plt.savefig(save_path)
    plt.close()

def save_images2(X, save_path,minn=None,maxx=None,img_num=0,p=0):
    # [0, 1] -> [0,255]
    n_samples = X.shape[0]
    #X=np.maximum(X,0)
    #X=cut_most(X,p)
    #X = cut_least(X, p)
    #print(X)
    if True:
        rows = int(np.sqrt(n_samples)) + 1
        while n_samples % rows != 0:
            rows -= 1

        nh, nw = int(rows), int(n_samples / rows)
    else:
        nh=int(img_num)
        nw=int(n_samples/img_num)
    if img_num==0:
        if minn is None:
            minn=np.min(X.reshape([X.shape[0],-1]),axis=1)
            maxx=np.max(X.reshape([X.shape[0],-1]),axis=1)
            if X.ndim == 4:
                minn=minn.reshape([X.shape[0],1,1,1])
                maxx=maxx.reshape([X.shape[0],1,1,1])
            elif X.ndim==3:
                minn = minn.reshape([X.shape[0], 1, 1])
                maxx = maxx.reshape([X.shape[0], 1, 1])
            else :
                minn = minn.reshape([X.shape[0], 1])
                maxx = maxx.reshape([X.shape[0], 1])

            X=(X-minn)/(maxx-minn+1e-8)
        else:
            X = (X - minn) / (maxx - minn + 1e-8)
            X=np.maximum(X,0)
            X=np.minimum(X,1)
    else:
        X_temp=X.reshape([nh,nw,-1])
        minn=np.min(X_temp,axis=0)
        minn=np.min(minn,axis=-1).reshape([1,-1,1,1,1])
        maxx=np.max(X_temp,axis=0)
        maxx=np.max(maxx,axis=-1).reshape([1,-1,1,1,1])
        #print(minn.shape, maxx.shape)
        X_temp = X.reshape([nh, nw, X.shape[1],X.shape[2],X.shape[3]])
        X_temp=(X_temp - minn) / (maxx - minn + 1e-8)
        X=X_temp.reshape(X.shape)
    #X = X.squeeze()
    #if isinstance(X.flatten()[0], np.floating):
    #    #X = (255 * X).astype('uint8')
    #    X=np.uint8(255 * X)



    if X.ndim == 2:
        X = np.reshape(X, (X.shape[0], int(np.sqrt(X.shape[1])), int(np.sqrt(X.shape[1]))))

    if X.ndim == 4:
        # BCHW -> BHWC
        X = X.transpose(0, 2, 3, 1)
        h, w = X[0].shape[:2]
        img = np.zeros((h * nh, w * nw, 3))
    elif X.ndim == 3:
        h, w = X[0].shape[:2]
        img = np.zeros((h * nh, w * nw))

    for n, x in enumerate(X):
        j = int(n / nw)
        i = int(n % nw)
        img[j * h:j * h + h, i * w:i * w + w] = x
    np.set_printoptions(threshold=np.inf)
    #print(save_path,img)
    #plt.imsave(save_path, img)
    #print(img.shape)

    #img=np.mean(img,2)

    #plt.imshow(img, cmap="seismic")#'jet'
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #im = ax.imshow(img)
    plt.imshow(img)
    plt.axis('off')
    # plt.gcf().set_size_inches(512 / 100, 512 / 100)
    plt.gcf().set_size_inches(img.shape[1] / 100, img.shape[0] / 100)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)
    #fig.tight_layout()
    plt.savefig(save_path)
    plt.close()


def save_images3(X, save_path,minn=None,maxx=None,img_num=0,p=0):
    # [0, 1] -> [0,255]
    n_samples = X.shape[0]
    #print(X.shape)
    X=np.sum(X,1)
    #X=np.abs(X)

    #plt.colorbar()

    #print(X)
    if True:
        rows = 1
        nh, nw = int(rows), int(n_samples / rows)
    '''
    if img_num==0:
        if minn is None:
            minn=np.min(X.reshape([X.shape[0],-1]),axis=1)
            maxx=np.max(X.reshape([X.shape[0],-1]),axis=1)
            if X.ndim == 4:
                minn=minn.reshape([X.shape[0],1,1,1])
                maxx=maxx.reshape([X.shape[0],1,1,1])
            elif X.ndim==3:
                minn = minn.reshape([X.shape[0], 1, 1])
                maxx = maxx.reshape([X.shape[0], 1, 1])
            else :
                minn = minn.reshape([X.shape[0], 1])
                maxx = maxx.reshape([X.shape[0], 1])

            X=(X-minn)/(maxx-minn+1e-8)
        else:
            X = (X - minn) / (maxx - minn + 1e-8)
            X=np.maximum(X,0)
            X=np.minimum(X,1)
    else:
        X_temp=X.reshape([nh,nw,-1])
        minn=np.min(X_temp,axis=0)
        minn=np.min(minn,axis=-1).reshape([1,-1,1,1,1])
        maxx=np.max(X_temp,axis=0)
        maxx=np.max(maxx,axis=-1).reshape([1,-1,1,1,1])
        #print(minn.shape, maxx.shape)
        X_temp = X.reshape([nh, nw, X.shape[1],X.shape[2],X.shape[3]])
        X_temp=(X_temp - minn) / (maxx - minn + 1e-8)
        X=X_temp.reshape(X.shape)
    '''


    if X.ndim == 4:
        # BCHW -> BHWC
        X = X.transpose(0, 2, 3, 1)
        h, w = X[0].shape[:2]
        img = np.zeros((h * nh, w * nw, 3))
    elif X.ndim == 3:
        h, w = X[0].shape[:2]
        img = np.zeros((h * nh, w * nw))

    for n, x in enumerate(X):
        j = int(n / nw)
        i = int(n % nw)
        img[j * h:j * h + h, i * w:i * w + w] = x
        img[:, i * w:i * w + 1] = 0
    np.set_printoptions(threshold=np.inf)
    #print(save_path,img)
    #plt.imsave(save_path, img)
    #print(img.shape)

    #img=np.mean(img,2)
    plt.imshow(img, cmap="seismic")
    high = np.abs(X).max()
    plt.clim(-high, high)
    #plt.imshow(img)
    plt.axis('off')
    plt.gcf().set_size_inches(img.shape[1] / 100,  img.shape[0]/ 100)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)
    plt.savefig(save_path)
    plt.close()
import numpy as np

G = [0, 255, 0]
R = [255, 0, 0]


def convert_to_gray_scale(attributions):
    return np.average(attributions, axis=2)


def linear_transform(attributions, clip_above_percentile=99.9, clip_below_percentile=70.0, low=0.2,
                     plot_distribution=False):
    m = compute_threshold_by_top_percentage(attributions, percentage=100 - clip_above_percentile,
                                            plot_distribution=plot_distribution)
    e = compute_threshold_by_top_percentage(attributions, percentage=100 - clip_below_percentile,
                                            plot_distribution=plot_distribution)
    transformed = (1 - low) * (np.abs(attributions) - e) / (m - e) + low
    transformed *= np.sign(attributions)
    transformed *= (transformed >= low)
    transformed = np.clip(transformed, 0.0, 1.0)
    return transformed


def compute_threshold_by_top_percentage(attributions, percentage=60, plot_distribution=True):
    if percentage < 0 or percentage > 100:
        raise ValueError('percentage must be in [0, 100]')
    if percentage == 100:
        return np.min(attributions)
    flat_attributions = attributions.flatten()
    attribution_sum = np.sum(flat_attributions)
    sorted_attributions = np.sort(np.abs(flat_attributions))[::-1]
    cum_sum = 100.0 * np.cumsum(sorted_attributions) / attribution_sum
    threshold_idx = np.where(cum_sum >= percentage)[0][0]
    threshold = sorted_attributions[threshold_idx]
    if plot_distribution:
        raise NotImplementedError
    return threshold


def polarity_function(attributions, polarity):
    if polarity == 'positive':
        return np.clip(attributions, 0, 1)
    elif polarity == 'negative':
        return np.clip(attributions, -1, 0)
    else:
        raise NotImplementedError


def overlay_function(attributions, image):
    return np.clip(0.7 * image + 0.5 * attributions, 0, 255)


def visualize(attributions, image, positive_channel=G, negative_channel=R, polarity='positive',
              clip_above_percentile=99.9, clip_below_percentile=0, morphological_cleanup=False,
              structure=np.ones((3, 3)), outlines=False, outlines_component_percentage=90, overlay=True,
              mask_mode=False, plot_distribution=False):
    if polarity == 'both':
        raise NotImplementedError

    elif polarity == 'positive':
        attributions = polarity_function(attributions, polarity=polarity)
        channel = positive_channel

    # convert the attributions to the gray scale
    attributions = convert_to_gray_scale(attributions)
    attributions = linear_transform(attributions, clip_above_percentile, clip_below_percentile, 0.0,
                                    plot_distribution=plot_distribution)
    attributions_mask = attributions.copy()
    if morphological_cleanup:
        raise NotImplementedError
    if outlines:
        raise NotImplementedError
    attributions = np.expand_dims(attributions, 2) * channel
    if overlay:
        if mask_mode == False:
            attributions = overlay_function(attributions, image)
        else:
            attributions = np.expand_dims(attributions_mask, 2)
            attributions = np.clip(attributions * image, 0, 255)
            attributions = attributions[:, :, (2, 1, 0)]
    return attributions