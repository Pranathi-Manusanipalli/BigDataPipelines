## Data As a Service
In this Assignment we have reviewed the Moody's Analytics portal to understand how APIs are designed and made the Nasa Turbofan Jet Engine Data available as an API

## Pipeline
![Pipeline](images/pipeline.png)

### Requirements - 
Install the dependencies as outlines in the requirements.txt by running 
`pip install -r requirements.txt`

### Resources used
* Python
* Snowflake
* FastAPI
* Airflow
* pytest
* Locust
* Diagrams


### Instructions to run
-  Basic usage of the API is available in 'main.py'
- Run the server with `uvicorn main:app --reload`
- Go to `http://127.0.0.1:8000/docs` and you should see the interactive API documentation
- Run the pytests defined in the 'test_main.py' file using the following commands

- `pytest -m configtest -v`  - To run the tests marked as 'configtest'
- `pytest -m starttest -v`  - To run the tests marked as starttest
- `pytest -m valuetest -v` - To run the tests marked as valuetests

- To do load testing using locust, run the command **`locust`** in the terminal which starts a web user interface at a specific port number, in our case it is localhost:8089

- Unittesting.ipynb -> Jupyter notebook to run API test cases

Detailed Claat Document - https://codelabs-preview.appspot.com/?file_id=1Xudq8lRNntqg1U7c-0w1jIf_eJcNshnpj5vEi0Zdwt0#0


