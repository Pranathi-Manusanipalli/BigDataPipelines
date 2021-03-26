import os
import boto3
import pandas as pd
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import re

def download():
  #initiate s3 resource
  s3 = boto3.resource('s3')


  # select bucket
  my_bucket = s3.Bucket('edgarfile-storage')

  parent_dir = "/Users/prathyusha/Desktop/pranathi/Assignment2"
  directory='edgar_download'
  # Path 
  localpath = os.path.join(parent_dir, directory) 

  if not os.path.exists(os.path.dirname(localpath)):
    os.makedirs(os.path.dirname(localpath))
    print("Directory '% s' created" % directory) 

  # download file into current directory
  for s3_object in my_bucket.objects.all():
      #print(s3_object.key)
      # Need to split s3_object.key into path and file name, else it will give error file not found.
      path, filename = os.path.split(s3_object.key)
      
      if filename in ('.DS_Store',''):
          continue
      else:
          my_bucket.download_file(s3_object.key, os.path.join(localpath,filename) )
  print("Download Completed")



def preprocess():

  DIR = "/Users/prathyusha/Desktop/pranathi/Assignment2/edgar_download"
  final_df=pd.DataFrame({'Text':[],'company':[]})

# if you want to list all the contents in DIR
  entries = [entry for entry in os.listdir(DIR)]
  #print(entries)
  for i in entries:
      #company=i
      #print(i)
      index_value=entries.index(i)
      string = open('{}'.format(os.path.join(DIR,i))).read()
      n=string.replace('\n\nCompany Representatives\n\n', '\n\nCompany Participants\n\n')
      n=n.replace('–', '-')
      n = n[n.find('Company Participants')+len('Company Participants'):]

      a = []
      start=''
      for line in n.split("\n"):
          if line != '' and '-' in line:
              a.append(line[0:line.find('-')])
          elif line != '' and '-' not in line and 'Conference Call Participants' not in line:
              start=line
              break
      if 'Conference Call Participant' in a:
          a.remove('Conference Call Participant')
      a=[re.sub('[^a-zA-Z0-9\s\n\.]', '', _) for _ in a]
      a=[i.strip() for i in a]
      a.append('Operator')
      a.append('Unidentified Analyst')
      split_list=string.split('\n\n')
      #print(company)
    #print(start)
      if start!='Operator':
          splitlist_new=split_list[split_list.index('{}'.format(start)):]
      else:
          splitlist_new=split_list[split_list.index('Operator'):]
      mainlist=[]
      company=[]

      for j in splitlist_new:
          if j not in a:
              mainlist.append(j)
              company.append(i)
      new_df=pd.DataFrame({'Text':mainlist})

      copy_df=new_df.copy()
      copy_df['company']=company
      def clean(row):
          return re.sub('[^a-zA-Z0-9\s\n\.]', '', row['Text'])
      copy_df['Text']=copy_df.apply(lambda row: clean(row),axis=1)
      copy_df=copy_df.dropna()
      copy_df['Text']=copy_df['Text'].str.strip()
      copy_df=copy_df[copy_df['Text']!='']
      
      final_df=pd.concat([final_df,copy_df])
  return final_df



def sentiment(final_df):
  headers = {
      # Request headers
      'Content-Type': 'application/json',
      'Ocp-Apim-Subscription-Key': 'f91e8d2d0a74487dbec98f4b8b302711',
  }

  params = urllib.parse.urlencode({
      # Request parameters
      'showStats': '{boolean}',
  })
  def positivity(row):
        
        
        #row['Text']=re.sub('[^a-zA-Z0-9\s\n\.]', '', row['Text'])
        #print(row['Text'])
        api_body={
          "documents": [
            {
              "language": "en",
              "id": "1",
              "text": row['Text']
            }
          ]
        }
        
        conn.request("POST", "/text/analytics/v2.1/sentiment?%s" % params, """{}""".format(api_body) , headers)
        response = conn.getresponse()
        data = response.read()
        #data_decoded=data.decode("utf-8") 
        data_decoded=json.loads(data)
        #print(data_decoded) 
        
        row['metric']=data_decoded['documents'][0]['score']

        return row
  conn = http.client.HTTPSConnection('eastus.api.cognitive.microsoft.com')
  copy_df=final_df.apply(lambda row: positivity(row),axis=1)
  conn.close()
  return copy_df





download()
final_df=preprocess()
#sentiment(final_df[1:10])
#print(final_df[1:10])
#print(sentiment(final_df[1:10]))