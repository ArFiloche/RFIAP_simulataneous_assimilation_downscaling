import torch
import numpy as np
import matplotlib.pyplot as plt

from .score_metrics import*
from .velcolor import*
from tabulate import tabulate


################# W

def plot_w(U,V,title = 'W',
           normalization=True,quiver=False,q_alpha = 0.5,q_scale =0.1,sub=4):
    
    x,y = np.meshgrid(np.arange(0,U.shape[0],sub),np.arange(0,U.shape[1],sub))

    plt.imshow(computeColor(U.numpy(),V.numpy(),norma = normalization))#,origin='lower')
    #plt.axis('off')
    
    if quiver:
        
        plt.quiver(y,x,U[x,y],-V[x,y],alpha = q_alpha,scale = q_scale)
        
    plt.title(title)
    plt.yticks([])
    plt.xticks([])

def plot_ssh(ssh_deep, ssh_hr,subtitle=''):
    
    plt.figure(figsize=(12,4))

    plt.subplot(1,3,1)
    plt.imshow(ssh_deep.squeeze(0), vmin=ssh_hr.min(), vmax=ssh_hr.max())
    plt.title('Estimate')
    plt.colorbar()

    plt.subplot(1,3,2)
    plt.imshow(ssh_hr, vmin=ssh_hr.min(), vmax=ssh_hr.max())
    plt.title('Ground Truth')
    plt.colorbar()

    plt.subplot(1,3,3)
    plt.imshow((ssh_hr-ssh_deep.numpy()))
    plt.title('Difference')
    plt.colorbar()
    
    plt.suptitle(subtitle, fontsize="x-large")
    
    
def plot_w_compare(w1,w2,
                   title1='w0 truth',title2='w0 assim',
                   normalization = True,quiver=False,q_alpha = 0.5,q_scale = 0.1):
    
    U1=w1[0,:,:]
    V1=w1[1,:,:]
    
    U2=w2[0,:,:]
    V2=w2[1,:,:]
    
    plt.subplot(1,3,1)
    plot_w(U1,V1,
           normalization=normalization,
           quiver=quiver, q_alpha=q_alpha,q_scale=q_scale,
           title = title1)
    
    plt.subplot(1,3,2)
    
    plot_w(U2,V2,
           normalization=normalization,
           quiver=quiver, q_alpha=q_alpha,q_scale=q_scale,
           title = title2)
    
    plt.subplot(1,3,3)
    plot_w(U1-U2,V1-V2,
           normalization=normalization,
           quiver=quiver, q_alpha=q_alpha,q_scale=q_scale,
           title = 'difference')
    
    plt.show()
    

def print_w_compare(w1,w2,method='4D-Var'):
    
    epe = EPE(w1,w2)
    aae = AAE(w1,w2)
    
    norm_gradw1=norm_gradw(w1)
    norm_gradw2=norm_gradw(w2)
    
    norm_divw1=norm_divw(w1)
    norm_divw2=norm_divw(w2)
    
    norm_lapw1=norm_lapw(w1)
    norm_lapw2=norm_lapw(w2)
    
    
    print(tabulate([[method, epe, aae, norm_gradw2,norm_divw2,norm_lapw2],
                ['Ground truth','0','0', norm_gradw1,norm_divw1,norm_lapw1]],
                headers=['Metric','Endpoint err.','Angular err. (°)',
                         '||grad||','||div||','||lap||'],
                tablefmt='orgtbl'))