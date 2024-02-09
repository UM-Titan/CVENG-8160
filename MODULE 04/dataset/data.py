import os,torch
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

def get_zscore(x, mu,std):
     return (x - mu)/std

class TrafficDataset(Dataset):
  def __init__(self,root_dir,csv_path):

    ## pass normalization as an input
    ## if user wants to transform pass normalization and to tensor.
    ## add day of week and hour.
    self.root_dir = Path(root_dir)
    self.csv_path = csv_path

    self.df = pd.read_csv(os.path.join(self.root_dir,self.csv_path))
    self.df = self.df[['detector_id', 'travelway','loc', 'datetime', 'speed', 'volume', 'occupancy', 'congested']]
    self.df = self.df[self.df['volume']>0]
    self.df['datetime'] = pd.to_datetime(self.df['datetime'])
    self.df = self.df.sort_values(by=['detector_id','loc','datetime'])
    # id = self.df['detector_id'].unique()[50:80]
    id = self.df['detector_id'].unique()
    self.df = self.df[self.df['detector_id'].isin(id)]

    for norm_cols in [('volume','volume_normal'),('occupancy','occu_normal')]:
      self.mu = self.df[norm_cols[0]].mean()
      self.std = self.df[norm_cols[0]].std()
      self.df[norm_cols[1]] = self.df.apply(lambda x: get_zscore(x[norm_cols[0]], self.mu,self.std),axis=1)

    # print (self.df.columns)
    # self.inputs = list(self.df['occu_normal'].values)
    # self.outputs = list(self.df['volume_normal'].values)
    
    self.inputs = list(self.df['volume_normal'].values)
    self.outputs = list(self.df['occu_normal'].values)

  def __len__(self):
    return len(self.df)

  def __getitem__(self,idx):
    X = self.inputs[idx]
    y=self.outputs[idx]

    return {'inputs':X,'outputs':y}

class ToTensor(object):
    def __call__(self, sample):
        input, output = sample['inputs'], sample['outputs']

        return {'inputs': torch.tensor(np.array(input),dtype=torch.float32).reshape(-1,1),
                'outputs': torch.tensor(np.array(output),dtype=torch.float32).reshape(-1,1)}