
# Import Needed Libraries
import uvicorn
import pandas as pd
from fastapi import FastAPI,Query
from pydantic import BaseModel
import tensorflow as tf
import logging
from pathlib import Path
import os
import numpy as np
import boto3
from smart_open import smart_open
import tensorflow_text
from typing import List
from fastapi.middleware.cors import CORSMiddleware

import json
from pydantic import BaseModel
import logging





# Initiate app instance
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def chunks(lst,n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


@app.get('/')
def root():
    return {'message':'Get Sentiment Predictions'}

@app.get('/download')
def download_model():
    s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id='AKIAJV5PIUOIYOJJ3VEQ', aws_secret_access_key='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')
    # select bucket
    local_dir = './Model/'
    bucket_name='prudhvics'
    prefix='model/'
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=prefix):
        target = obj.key if local_dir is None \
            else os.path.join(local_dir, os.path.relpath(obj.key, prefix))
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        if obj.key[-1] == '/':
            continue
        bucket.download_file(obj.key, target)

# Prediction endpoint
@app.post('/predict')
def get_prediction(data: List[str]= Query(None)):
    data=data
    # Make predictions based on the incoming data and saved neural net
    model_path = './Model/'
    checkpoint = tf.saved_model.load(model_path)
    f = checkpoint.signatures["serving_default"]
    predict = f(tf.constant([data]))
    value = list(predict.values())[0].numpy()
    # print(predict.values())
    value=[item for sublist in value for item in sublist]
    print(value)
    value=[round(float(i),3) for i in value]
    # preds = get_prediction(data)
    print(value)
    # Return the predicted class and the predicted probability
    return {'sentiment':value}
#
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

@app.get("/get_prediction")
async def get_prediction(s3_url: str):



    aws_access_key_id = 'AKIAJV5PIUOIYOJJ3VEQ'
    aws_secret_access_key = 'LfR3OY+MWpXjZ91yTUK8I0MCmsCTOHzoHgAdGaoQ'
    bucket_name ='prudhvics'
    object_key = s3_url.split('//')[1].replace(bucket_name+'/','')
    path = 's3://{}:{}@{}/{}'.format(aws_access_key_id, aws_secret_access_key, bucket_name, object_key)
    df = pd.read_csv(smart_open(path),sep='\n')
    df=df.dropna()
    df.columns = ['Text']
    #print(df)
    listtext=list(df["Text"])
    listtext=listtext[:150]

    model_path = './Model/'
    checkpoint = tf.saved_model.load(model_path)
    f = checkpoint.signatures["serving_default"]




    final_df=pd.DataFrame({"Text":[],"metric":[]})

    for lis in chunks(listtext,200):
        predict = f(tf.constant([lis]))
        value = list(predict.values())[0].numpy()
        #r = requests.post("http://localhost:8000/predict",data=lis)
        #a = json.loads(value)
        copy_df=final_df[final_df["Text"]=='~~~']
        copy_df["Text"]=lis
        copy_df["metric"]=value
        final_df=pd.concat([final_df,copy_df])

    #print(final_df)
    return {'Text':list(final_df['Text']),
                        'metric': list(final_df['metric'])}

if __name__ == "__main__":
    # Run app with uvicorn with port and host specified. Host needed for docker port mapping
    uvicorn.run(app, port=8000, host="0.0.0.0")

