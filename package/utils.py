import pandas as pd 
import os

# for visualization
import folium
from folium.plugins import HeatMap
from folium import plugins
import seaborn as sns
import matplotlib.pyplot as plt
from ipywidgets import interact, widgets

class Titan:
  def __init__(self,csv_path):
        # call super() function
        super().__init__()
        self.csv_path = csv_path
        self.df = None
        self.df_formatted = None
  # pass
  def read_csv(self,**kwargs):
    # print (kwargs)
    ## kwargs: read_csv(row=5, x=5,y=40): calling-- kwargs[x] 
    ## args: read_csv(5)
    if kwargs:
      print ('reading {} rows of data'.format(kwargs['nrows']))
      self.df = pd.read_csv(self.csv_path,nrows=kwargs['nrows']) 
    else:
      print ('reading all rows of data. This might take time')
      self.df = pd.read_csv(self.csv_path)

    # return self.df 
    return self
   
  def format_csv(self):

    # self.df = self.read_csv()
    self.df_formatted = self.df.copy()
    

    out_columns = ['eventId', 'type', 'main', 'cross', 'descripton','longitude', 'latitude',
        'start', 'estStop', 'clear']
    
    # print (self.df)
    
    self.df_formatted.columns = out_columns
    
    self.df_formatted['start'] = pd.to_datetime(self.df_formatted['start'])
    
    self.df_formatted['estStop']= pd.to_datetime(self.df_formatted['estStop'])
    self.df_formatted['clear']= pd.to_datetime(self.df_formatted['clear'])
    
    self.df_formatted['duration'] = (self.df_formatted['clear'] - self.df_formatted['start']).astype('timedelta64[m]')
    
    self.df_formatted = self.df_formatted[self.df_formatted['main']=='AccidentsAndIncidents']
    self.df_formatted = self.df_formatted[self.df_formatted['duration']>0]

    self.df_formatted['year'] = self.df_formatted['start'].dt.year
    self.df_formatted['dow'] = self.df_formatted['start'].dt.weekday
    self.df_formatted['hour'] = self.df_formatted['start'].dt.hour
    self.df_formatted = self.df_formatted[self.df_formatted['duration']<120]
    

    self.df_formatted['latitude']= self.df_formatted['latitude'].astype(int)/1000000
    self.df_formatted['longitude']= self.df_formatted['longitude'].astype(int)/1000000
    max_amount = float(self.df_formatted['duration'].max())
    
    return self
    # return self.__class__ 

  def point_map(self,*args):
    if len(args)>0:
      df_ = self.df_formatted.head(args[0])
    else:
      df_ = self.df_formatted.copy()
    # print (args)
    mx = folium.Map([38.6, -90.199], zoom_start=11)
    for index, row in df_.iterrows():
        folium.CircleMarker([row['latitude'], row['longitude']],
                            radius=2,
                            popup=row['main'],
                            fill_color="#3db7e4", # divvy color
                          ).add_to(mx)
    
    return mx

  def heat_map(self,*args):
    if len(args)>0:
      df_ = self.df_formatted.head(args[0])
    else:
      df_ = self.df_formatted.copy()

    my = folium.Map([38.6, -90.199], zoom_start=10)
    stationArr = df_[['latitude', 'longitude']].to_numpy()
    my.add_children(plugins.HeatMap(stationArr, radius=10,max_val=30))
    return my 
  def get_road_rank(self):
    def g(x):
      df_top = self.df_formatted.groupby(['cross']).agg({'eventId':'count'}).reset_index()
      df_top = df_top.sort_values(by='eventId',ascending=False).head(x)
      fig, ax = plt.subplots(figsize=(2*x,x))
      img = sns.barplot(x='cross', y='eventId', data=df_top, palette='summer',ax=ax)
      return img
    # interact(g,x=10)
    interact(g,x=widgets.IntSlider(min=5, max=30, step=5, value=10))

  def get_duration_heatmap(self):
    def f(x):
      ## filter by road, by dropdown
      df = self.df_formatted[self.df_formatted['cross'] == x]
      df_grp = df[['dow','hour','duration']].groupby(['dow','hour']).agg({'duration':'mean'}).reset_index()
      df_grp.columns = ['dow','hour','count']
      result = df_grp.pivot(index='dow', columns='hour', values='count')
      fig, ax = plt.subplots(figsize=(30,10))
      img = sns.heatmap(result, annot=False, fmt="g", cmap='viridis', ax=ax)
      return img
    interact(f,x=['I-70 EB', 'I-64 WB', 'I-270 NB', 'I-64 EB', 'I-70 WB'])

  def get_crashes_heatmap(self):
    def f(x):
      ## filter by road, by dropdown
      df = self.df_formatted[self.df_formatted['cross'] == x]
      df_grp = df[['dow','hour','eventId']].groupby(['dow','hour']).agg({'count'}).reset_index()
      df_grp.columns = ['dow','hour','count']
      result = df_grp.pivot(index='dow', columns='hour', values='count')
      fig, ax = plt.subplots(figsize=(20,10))
      img = sns.heatmap(result, annot=True, fmt="g", cmap='viridis', ax=ax)
      return img
    interact(f,x=['I-70 EB', 'I-64 WB', 'I-270 NB', 'I-64 EB', 'I-70 WB'])
  def get_crashes_year_heatmap(self):
    def f(x):
      ## filter by road, by dropdown
      df = self.df_formatted[self.df_formatted['year'] == x]
      df_grp = df[['dow','hour','eventId']].groupby(['dow','hour']).agg({'count'}).reset_index()
      df_grp.columns = ['dow','hour','count']
      result = df_grp.pivot(index='dow', columns='hour', values='count')
      fig, ax = plt.subplots(figsize=(20,10))
      img = sns.heatmap(result, annot=True, fmt="g", cmap='viridis', ax=ax)
      return img
    interact(f,x=widgets.IntSlider(min=self.df_formatted['year'].min(), 
                                   max=self.df_formatted['year'].max(), 
                                   step=1, value=self.df_formatted['year'].min()))