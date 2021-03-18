### FastAPI
In this Lab, we are going to learn how to use FastAPI framework for building APIs

#### What is FastAPI? 

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

#### Requirements

```
pip3 install fastapi
pip3 install uvicorn
pip3 install iexfinance
```
#### Content
- **Usecase 1** - Demonstrates simple API to fetch and create items
    - main.py -> Cotains the basic usage code of API with all the required routing logic

- **Usecase 2** 
Prerequisite - Create a DynamoDB table named `customer-trades` with `id` as unique identifier
     -   id_generator.py -> Script to generate unique 10 digit alpha-numeric ID
    -   stock_price.py ->  Python script to get the current stock price of a given company
    -   trades.py -> Script to deploy the FastAPI endpoint. 


### Instructions to run 
- Run the server with `uvicorn main:app --reload`. 

    For the second usecase replace `main` with `trades` as it contains the routing logic 
`uvicorn trades:app --reload`

- Go to `http://127.0.0.1:8000/docs` and you should see the interactive API documentation.

##### CLAT Document - 
Refer to <> for detailed documentation of the lab