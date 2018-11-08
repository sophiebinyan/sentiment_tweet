import pandas as pd
import tarfile
#import dataset # Using dataset as I'm still iteratively developing the table structure(s)
import bz2
import json
import datetime
import numpy as np
import re
###################################
###############function scrape tar
###################################
def scrape_tar_contents(tar_filename,to_path):
  print 'opening'
  tar = tarfile.open(tar_filename, 'r')
  print 'inner file'
  inner_files = [filename for filename in tar.getnames() if filename.endswith('.bz2')]
  num_bz2_files = len(inner_files)
  print "{} .bz2 files in the tar file".format(num_bz2_files)
  bz2_count = 1
  print('Starting work on bz2 files... ')
  # Loop over all files in the TAR archive
  r=[]
  flag=0
  for i,bz2_filename in enumerate(inner_files):
    if np.mod(i,100)==0:
      print 'starting work on the {}/{} inner file: {}'.format(i+1,num_bz2_files,bz2_filename)
    t_extract = tar.extractfile(bz2_filename)
    data = t_extract.read()
    txt = bz2.decompress(data)
   
    tweet_errors = 0
    current_line = 1
    num_lines = len(txt.split('\n'))
    #loop over the lines in the extracted text file
    for line in txt.split('\n'): 
      #if current_line % 100 == 0:
      #  print 'working on line {}/{}'.format(current_line,num_lines)
      try:
        tweet=json.loads(line)
      except ValueError, e: #to store errors in a log file
        error_log = {'Date_time': datetime.datetime.now(),
                    'File_TAR': filename,
                    'File_BZ2': bz2_filename,
                    'Line_number': current_line,
                    'Line': line,
                    'Error': str(e)}
        tweet_errors += 1
        #print 'Error occured, now at line {}'.format(current_line)
        #error ocurred because the tweet has been deleted
      try:
        if tweet['geo'] is not None:
          tweet_coor=tweet['geo']['coordinates']
        else:
          if tweet['place'] is not None:
            if tweet['place']['bounding_box'] is not None:  
              tweet_coor=tweet['place']['bounding_box']['coordinates']
            else:
              continue
          else:
            continue
        if tweet['lang']=='en':
          st=tweet['text'].encode('utf-8')
          st = re.sub('[\n]', ' ', st)
          r.append([tweet['id'],tweet['created_at'],tweet_coor,st])
          if len(r)%1000==0:
            pd.DataFrame(r).to_csv('{}output_{}.csv'.format(to_path,flag))
            r=[]
            flag+=1
        else:
          continue
      except KeyError, e:
        error_log = {'Date_time': datetime.datetime.now(),
                    'File_TAR': filename,
                    'File_BZ2': bz2_filename,
                    'Line_number': current_line,
                    'Line': line,
                    'Error': str(e)}
        tweet_errors += 1
        #print 'Error occured, now at line {}'.format(current_line)
      current_line+=1
    #print bz2_filename
    #print 'total number of errors is {}'.format(tweet_errors)
    #print r 
    #print (len(r))
    if len(r)>0:
      pd.DataFrame(r).to_csv('{}output_{}.csv'.format(to_path,flag))
################main
if __name__ == "__main__":
  #tar_filename='../data/archiveteam-twitter-stream-2018-01.tar'
  tar_filename='../data/201712.tar'
  to_path='../processed_data/filtered_data_geo/201712/'
  print tar_filename
  scrape_tar_contents(tar_filename,to_path)
