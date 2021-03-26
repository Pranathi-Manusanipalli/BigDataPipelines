# Sentiment Analysis Flask API:

The main aim of this module is to download the trained tensorflow from s3 bucket and expose it as Flask API for inference.

***Technical Requirements:***
- Docker pre-installed
- s3 bucket access

***Python Files:***
- api: app.py - Initialises the Flask app based on a blueprint
- api: ml_app.py - The entire blueprint of the flask app withn POST and GET methods
- saved_models: load_model.py - Contains the code which loads the model
- config.yaml - Contains the dynamic parameters for the app execution
- loadyaml.py - Contains the code to load a specified yaml file
- predict.py - Contains the code to get loaded model do the predictions and return the results
- s3_download.py - Contains the code to download model from s3 bucket
- Dockerfile - Contains the steps required for dockerizing the application
- run.py - The main file where the app execution starts

***Steps to follow:***
- git clone the repository
- create a python3.7 environment using

    `pip3.7 install virtualenv`
    
    `python3.7 -m virtualenv venv`
    
    `source venv/bin/activate`
    
 - `pip install requirement.txt`
 
 - Dockerizing Application

    `docker build -t <imagename> .`
  
    `docker run -d -p 5000:5000 imagename`
  
Now the sentiment API is up and running and can be connected on http://0.0.0.0:5000/predict

***Deploying the app on Google Cloud Run:***<br>

- Install Google Cloud SDK 
- Authenticate the SDK using<br>
  `google auth login`<br>
- Authenicate docker to push images to Google Cloud Container Repositories<br>
  `google auth configure-docker`<br>
- Create a tag for your image<br>
  `docker tag imagename us.gcr.io/project-id/imagename` <br>
- Push the docker image<br>
  `docker push us.gcr.io/project-id/imagename` <br>
- Now to go to Cloud run and create a service with following parameters: <br>
  select the image from the container repository which we pushed<br>
  Memory: min 4GB<br>
  Create<br>
- Once Cloud Run service is created we will get the service url and our API is up and running<br>
- To access the API use `SERVICE URL/predict`<br>

***Claat Document:*** https://codelabs-preview.appspot.com/?file_id=1jCLBg9N-M6sL1eEP3I5kE4cvZVNoPEeiTT1aiGq8qdY#0
