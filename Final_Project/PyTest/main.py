import uvicorn
import pandas as pd
from fastapi import FastAPI,Query
from google.cloud import storage
import os
import pickle
import sklearn
from typing import List


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="bigdata-311523-d08f734796f8.json"
storage_client = storage.Client()

app = FastAPI()

@app.get('/')
def root():
    return {'message':'Get Category Prediction'}

# Download the model
@app.get('/download')
def download_model():
    bucket_name = 'invoices_image'
    prefix = 'model/'

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)  # Get list of files
    for blob in blobs:
        filename = blob.name 
        blob.download_to_filename(filename)  # Download
    return {'message':'Model Downloaded'}


# Prediction endpoint to predict the categories for given list of descriptions
@app.post('/predict')
def predict(data: List[str]= Query(None)):
    # Downloading the model 
    bucket_name = 'invoices_image'
    prefix = 'model/'
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)  # Get list of files
    for blob in blobs:
        filename = blob.name 
        blob.download_to_filename(filename)  # Download

    # Prediction
    data=data
    workdir = './model/'
    vectorizer_new=pickle.load(open(workdir + 'vectorizer.sav', "rb"))
    classifier_new=pickle.load(open(workdir + 'classifier.sav', "rb"))
    test = vectorizer_new.transform(data)
    output=classifier_new.predict(test).tolist()
    return {'predicted':output}


if __name__ == "__main__":
    # Run app with uvicorn with port and host specified. Host needed for docker port mapping
    uvicorn.run(app, port=8000, host="0.0.0.0")



   