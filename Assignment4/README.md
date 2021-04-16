## Model as a Service for anonymized data

In this assignment we are masking and anonymization the EDGAR data and deploying a sentiment analysis model to create a Model-as-a-service for the anonymized data. 


### Resources used
* Python
* FastAPI
* Streamlit
* AWS Lambda, Cognito
* Docker

For testing 
* pytest
* Locust



### Folder Structure - 




### Instructions to run - 
Mask_AnonymizeAPI 
* Install the dependecies by running ` pip install -r requirements.txt`
* Go to the folder containing the main.py file containing the basic API usage code, which in our case is `cd edgar/api`
* Now, start the fastapi by running `uvicorn main:app --reload`
* Go to `http://127.0.0.1:8000/docs` and you should see the interactive API documentation for the 3 routes defined
`/api1` - Takes the s3 url and fetch the data
`/api2` - Takes the s3 url as input and outputs the list of entities detected and store back to s3
`/api3` - Takes the list of entities that needs to be anonymized and masked as inputs and outputs the files back to s3 with the data anonymized and masked.


ModelServingAPI
* Install the dependecies by running ` pip install -r requirements.txt`
* Running the TFX Pipeline using Albert model pretrained on IMDB data and testing using our EDGAR data, results in a model which is saved in s3
* The Model Serving API can be started by running `uvicorn main:app --reload`.
`/download` - Downloads the model from s3 to local which is then used in our prediction 
`/predict` - Using the saved model, we do the sentiment prediction in this route by passing list of strings

This API needs to be dockerized as 
 - Dockerizing Application

    `docker build -t <imagename> .`
  
    `docker run -d -p 8000:8000 imagename`
Now the sentiment API is up and running and can be connected on http://0.0.0.0:8000/predict

Streamlit
* Install the dependecies by running ` pip install -r requirements.txt`
* Start the web application by running the following command
` streamlit run main.py`

Unittesting
* Install the dependecies by running ` pip install -r requirements.txt`
* Run the pytests defined in the 'test_main.py' file using the following commands
`pytest -m valuetest -v`
* To do load testing using locust, run the command **`locust`** in the terminal which starts a web user interface at a specific port number, in our case it is localhost:8089

Detailed Claat Document - https://codelabs-preview.appspot.com/?file_id=1d3v1_H75l7_SEldPHcDvTksFhZpgHmQW9e2eDJ4_93g#0

