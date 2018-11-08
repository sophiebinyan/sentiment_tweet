##########
#remember to remove duplicate records
###########
import glob
import pandas as pd
import gc
import json
import csv
import re
import numpy as np

#for sentiment
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from sentimenticon import sentiment #user contributed module

#for time
import time
from dateutil import tz
from datetime import datetime
import pytz
#from tzwhere import tzwhere #tzwhere is super slow
from timezonefinder import TimezoneFinder #user contributed module, a light version of tzwhere
import reverse_geocoder as rg

###############################
##1.coordinate
###############################
def point_coor(x):
  a=x.split('[')[1].split(']')[0].split(', ')
  return [np.round(np.float(a[1]),3),np.round(np.float(a[0]),3),'point']

def process_lon(x):
  if np.max(x)-np.min(x)>10:
    if x[np.argmax(np.abs(x))]>0:
      return 0.5*(np.min(x)-np.max(x))
    else:
      return 0.5*(np.max(x)-np.min(x))
  else:
    return np.mean(x)

def polygon_coor(x):
  #need to revise the method for calculating the center of a polygon
  a=x.split('[[[')[1].split(']]]')[0].split('], [')
  b=pd.DataFrame([i.split(', ') for i in a]).astype('float')
  return [np.round(process_lon(b[0].values),3),np.round(np.mean(b[1].values),3),'polygon']

def process_coor(coor): #coor is a list
  return [polygon_coor(x) if x.startswith('[[[') else point_coor(x) for x in coor]

###############################
##2.sentiment
###############################
def cal_sentiment(text):
  analyzer=sentiment.Analyzer()
  a=[re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", x) for x in text]
  s=[[round(analyzer.average_word_sentiment(x.split()),5),bool(re.search(' climate ',x)),bool(re.search(r'hurricane|harvey| storm |flooding| flood ',x)),bool(re.search(r'weather| rain| sunny | wind | windy ',x))] for x in a]
  return s

###############################
##3.time
###############################
def extract_time(t,lon,lat):
  from_zone = tz.tzutc()
  tf = TimezoneFinder()
  ts=[time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(date_string,'%a %b %d %H:%M:%S +0000 %Y')) for date_string in t]
  utc=[datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in ts]
  timezone_str=[tf.timezone_at(lng=lon[i],lat=lat[i]) for i in range(len(lon))]

  to_zone=[pytz.timezone(x) if x is not None else pytz.timezone('UTC') for x in timezone_str]
  local_time=[utc[i].replace(tzinfo=from_zone).astimezone(to_zone[i]) for i in range(len(to_zone))]
  return [[x.year,x.month,x.day,x.hour,x.minute] for x in local_time]

###############################
##driver
###############################
def driver(path,to_path,st_append):
  filenames = glob.glob(path + "/*.csv")
  id_list=[]
  coor_list=[]
  t_list=[]
  sentiment_list=[]
  city_state=[]
  for i,filename in enumerate(filenames):
    if i%100==0:
      print 'now processing file {}/{}'.format(i,len(filenames))
    with open(filename, 'rU') as csvfile:
      reader = csv.DictReader(csvfile)
      a=pd.DataFrame([[row['0'],row['1'],row['2'],row['3']] for row in reader]).dropna() #.encode('utf-8')
      a.columns=['id','time','coor','text']
    id=a['id'].values
    t=a['time'].values
    coor=a['coor'].values
    text=a['text'].values

    #processing
    processed_coor=process_coor(coor)
    lonlat=pd.DataFrame(processed_coor)[[0,1]]
    coor_list=coor_list+processed_coor
    id_list.extend(id)
    sentiment_list=sentiment_list+cal_sentiment(text)
    t_list=t_list+extract_time(t,list(lonlat[0].values),list(lonlat[1].values))

    coor_for_location=[(lonlat.iloc[k][1],lonlat.iloc[k][0]) for k in range(len(lonlat))]
    location=rg.search(coor_for_location)
    city_state=city_state+[[x['name'],x['admin2'],x['admin1'],x['cc']] for x in location] 
  r=[]
  for i in range(len(id_list)):
    r.append(coor_list[i]+[id_list[i]]+sentiment_list[i]+t_list[i]+city_state[i])
  df=pd.DataFrame(r,columns=['lon','lat','type','id','sentiment','climate','hurricane','weather','year','month','day','hour','minute','city','county','state','country'])
  df=df[df['country']=='US'] ##only keep US
  df.to_csv('{}{}.csv'.format(to_path,st_append))
  return
      
 
if __name__ == "__main__":
  
  path='../processed_data/filtered_data_geo/'
  to_path='../processed_data/test/'
  st_append=['201705','201706','201707','201708','201709','201710','201711','201712','201801','201802','201803','201804']
  for st in st_append:
    print st
    driver(path+st+r'/',to_path,st)
