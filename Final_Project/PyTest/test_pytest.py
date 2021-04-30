import pytest
from starlette.testclient import TestClient
from confest import test_app
import json
import requests
import os
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="bigdata-311523-d08f734796f8.json"
storage_client = storage.Client()

@pytest.mark.valuetest
def test_root(test_app):
    directory = os.path.dirname(os.path.realpath(__file__))
    print(directory)
    model_path=directory+"/model"
    if not os.path.exists(model_path):
        os.makedirs(model)
    response = test_app.get("/download")
    assert response.status_code == 200
    assert response.json() == {"message": "Model Downloaded"}


@pytest.mark.valuetest
def test_predict(test_app):
    directory = os.path.dirname(os.path.realpath(__file__))
    print(directory)
    model_path=directory+"/model"
    if not os.path.exists(model_path):
        os.makedirs(model)
    response = test_app.post("/predict?data=biryani")
    assert response.status_code == 200
    assert response.json() == {
  "predicted": [
    "Other Supplies Materials Equipment"
  ]
}

