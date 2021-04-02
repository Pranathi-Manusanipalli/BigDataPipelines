
import pytest
from starlette.testclient import TestClient
from confest import test_app
import json
import requests
import os
#from itertools import iterator

# response =requests.get("http://127.0.0.1:8000/generatetoken")
# Key = json.dumps(response.json())

@pytest.mark.valuetest
def test_cycles(test_app):
    
    response1 = test_app.get("/cycles?unit_number=1&fault=FD001")
    assert response1.status_code == 200
    assert response1.json() == {
  		"train_cycles": 192,
  		"test_cycles": 31
			}

@pytest.mark.valuetest
def test_root(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {
  "message": "Welcome to NASA Turbofan Jet Engine Data"
		}

@pytest.mark.configtest
def test_config(test_app):
    response = test_app.post("/pipeline/config")
    assert response.status_code == 200
    assert response.json() == [
  "Airflow Webserver & Scheduler Started"
]

@pytest.mark.starttest
def test_start(test_app):
    response = test_app.post("/pipeline/start")
    assert response.status_code == 200
    assert response.json() == {
  "status": "Airflow Pipeline Started",
  "details": 256
		}



@pytest.mark.valuetest
def test_rul(test_app):
    response = test_app.get("/rul?unit_number=1&fault=FD001")
    assert response.status_code == 200
    assert response.json() == [
  {
    "UNIT_NUMBER": 1,
    "FAULT": "FD001",
    "RUL": 112
  }
]


@pytest.mark.valuetest
def test_operational_data(test_app):
    response = test_app.get("/engine/operational_data?unit_number=1&dataset_type=train&fault=FD001")
    json_response = response.json()
    iterator = iter(json_response)
    val=True
    for x in iterator:
        if (x['FAULT']=='FD001') and (x['UNIT_NUMBER']==1):
            continue
        else:
            print(x)
            val=False
        
    if val==True:
        print('Succesful')
    assert response.status_code == 200
    assert val == True

@pytest.mark.valuetest
def test_sensordata(test_app):
    response = test_app.get("/engine/sensordata?unit_number=1&dataset_type=train&fault=FD001")
    json_response = response.json()
    iterator = iter(json_response)
    val=True
    for x in iterator:
        if (x['FAULT']=='FD001') and (x['UNIT_NUMBER']==1) :
            continue
        else:
            print(x)
            val=False
        
    if val==True:
        print('Succesful')
    assert response.status_code == 200
    assert val == True
