
import urllib.request, json 
import os
# Import Custom Modules
import boto3
import pandas as pd
import numpy as np
import json
import re
import sys
import yaml
import http.client, urllib.request, urllib.parse, urllib.error, base64
from smart_open import smart_open
import requests
#from flask import jsonify

yaml_path='/Users/prathyusha/Desktop/pranathi/CSYE7245-Spring2021-Labs/transcript-simulated-api/airflow/dags/config.yaml'

def load_yaml(yaml_path):
    try:
        with open(yaml_path, "r") as f:
            configs = yaml.safe_load(f)
    except Exception as e:
        print("Failed to load a yaml file due to {e}")
    return configs

config= load_yaml(yaml_path)

def getlist():
	aws_access_key_id = config["dev"]["aws_access_key_id"]
	aws_secret_access_key = config["dev"]["aws_secret_access_key"]
	bucket_name = config["dev"]["bucket"]
	object_key = config["dev"]["fileinput"]["object_key"]
	prefix = config["dev"]["fileinput"]["prefix"]
	path = 's3://{}:{}@{}/{}/{}'.format(aws_access_key_id, aws_secret_access_key, bucket_name, prefix, object_key)
	df = pd.read_csv(smart_open(path))
	print(df)
	df.to_csv("./companies_list.csv",index=False)


def download():
	df=pd.read_csv("./companies_list.csv")
	for company in list(df['company']):
		with urllib.request.urlopen("http://127.0.0.1:8000/call-transcripts/{}/2021".format(company)) as url:
			data = json.loads(url.read().decode())
			#print(data)
		parent_dir = config["dev"]["downloadpath"]
		directory='edgar_download' 
		localpath = os.path.join(parent_dir, directory) 
		print(localpath)
		if not os.path.exists(localpath):
			print("inside if")
			os.mkdir(localpath) 
		
		with open('{}/{}'.format(localpath,data["company"]), 'w') as f:
			f.write(data['transcript'])
		f.close()



def preprocess():

  #DIR = "/Users/prathyusha/Desktop/pranathi/Assignment2/airflow_edgar/edgar_download"

  DIR= config["dev"]["fetchpath"]
  final_df=pd.DataFrame({'Text':[],'company':[]})
  final_df=final_df[1:10]
# if you want to list all the contents in DIR
  entries = [entry for entry in os.listdir(DIR) if '.' not in entry]
  print(entries)
  #if entries in ('.DS_Store')
  for i in entries:
      #company=i
      #print(i)
      index_value=entries.index(i)
      #print(os.path.join(DIR,'{}'.format(i)))
      string = open(os.path.join(DIR,'{}'.format(i)),encoding='utf-8').read()
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
  aws_access_key_id = config["dev"]["aws_access_key_id"]
  aws_secret_access_key = config["dev"]["aws_secret_access_key"]
  bucket_name = config["dev"]["bucket"]
  object_key = config["dev"]["stage"]["object_key"]
  jsonobject_key=config["dev"]["stage"]["jsonobject_key"]
  prefix = config["dev"]["stage"]["prefix"]

  path = 's3://{}/{}/{}'.format(bucket_name, prefix, object_key)
  jsonpath = 's3://{}/{}/{}'.format(bucket_name, prefix, jsonobject_key)
  print(jsonpath)
  #print(final_df)

  final_df.to_csv(path,index=False)
  #final_df.reset_index(inplace=True)
  final_df.to_json("./companiesdata.json",orient = 'records', compression = 'infer', index = 'true')
  
  #temp=final_df.to_json(orient = 'records', compression = 'infer', index = 'true')
  #print(temp)

def prediction():
  aws_access_key_id = config["dev"]["aws_access_key_id"]
  aws_secret_access_key = config["dev"]["aws_secret_access_key"]
  bucket_name = config["dev"]["bucket"]
  object_key = config["dev"]["stage"]["object_key"]
  prefix = config["dev"]["stage"]["prefix"]
  path = 's3://{}:{}@{}/{}/{}'.format(aws_access_key_id, aws_secret_access_key, bucket_name, prefix, object_key)
  df = pd.read_csv(smart_open(path))
  df=df.dropna()
  listtext=list(df["Text"])
  #listtext=listtext[0:100]
  #print(listtext)
  #response = requests.post('http://0.0.0.0:5000/predict',json={"data": df1})
  #print(response.text)
  #a=json.loads(response.text)
  #print(a['pred'])
  #df1={"data":"this workshop is fun"}
  #print(df1["data"])
  def chunks(lst,n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

  session = requests.Session()
  for lis in chunks(listtext,50):
    print(len(lis))
    #r = session.post('http://0.0.0.0:5000/predict',json={"data": [lis]})
    #print(r.text)


  # session = requests.Session()
  # r = session.post('http://0.0.0.0:5000/predict', data=listtext)
  # print(r.)
  # o = session.post('http://0.0.0.0:5000/predict', data=listtext)

prediction()



#getlist()
#download()
#preprocess()




