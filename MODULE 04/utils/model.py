import os
import pandas as pd
import numpy as np
from torch.utils.data import DataLoader
import warnings
import torch
import torch.nn as nn
from tqdm import tqdm
from dataset.data import ToTensor
from sklearn.metrics import mean_absolute_percentage_error
warnings.filterwarnings("ignore")

def inv_zscore(preds, mu,std):
  preds = [(i*std)+mu for i in preds]
  return preds

def build_model(traffic_obj,bs,model,criterion,optimizer,n_epochs):
  dataloader = DataLoader(traffic_obj, batch_size=bs, shuffle=False, num_workers=4,drop_last=True)
  mean_loss = []
  losses = []
  ts = ToTensor()
  for it in tqdm(range(n_epochs)):
    # zero the parameter gradients
    for i_batch, sample_batched in enumerate(dataloader):
      optimizer.zero_grad()
      sample_batched = ts(sample_batched)
      outputs = model(sample_batched['inputs'])
      loss = criterion(outputs, sample_batched['outputs'])
      losses.append(loss.item())

      loss.backward()
      optimizer.step()
    mean_loss.append(np.mean(losses))
    print(f'Epoch {it+1}/{n_epochs}, Loss: {loss.item():.4f}')

  return model,losses, mean_loss
  
class Predict(object):
  def __init__(self,model,mu,std,plot=0):
    self.plot = plot
    self.model = model
    self.ts = ToTensor()
    self.preds = []
    self.targets = []
    self.mu = mu
    self.std = std 
  
  def __call__(self,sample):
    for i_batch, sample_batched in enumerate(sample):
      sample_batched = self.ts(sample_batched)
      outputs = self.model(sample_batched['inputs'])
      self.preds = self.preds + outputs.reshape(-1).tolist()
      self.targets = self.targets + sample_batched['outputs'].reshape(-1).tolist()
      
      ori_pred = inv_zscore(self.preds, self.mu,self.std)
      ori_target = inv_zscore(self.targets, self.mu,self.std)
      
      mape = mean_absolute_percentage_error(ori_target, ori_pred)

    return {'preds':np.array(self.preds),'targets':np.array(self.targets), 'mape':mape}