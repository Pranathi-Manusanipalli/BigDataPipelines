import pytest
from starlette.testclient import TestClient
from confest import test_app
import json
import requests
import os



@pytest.mark.valuetest
def test_root(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {'message':'Get Sentiment Predictions'}


@pytest.mark.valuetest
def test_predict(test_app):
    response = test_app.post("/predict?data=sad&data=happy")
    assert response.status_code == 200
    assert response.json() == {'sentiment':
        [
            0.589,
            0.585
        ]
    }


#pytest -m valuetest -v
