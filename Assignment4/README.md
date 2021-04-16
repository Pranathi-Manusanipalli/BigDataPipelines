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
* 


ModelServingAPI
* Install the dependecies by running ` pip install -r requirements.txt`

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

