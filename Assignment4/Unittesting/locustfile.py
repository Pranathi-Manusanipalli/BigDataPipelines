from locust import HttpUser, task, between
from starlette.testclient import TestClient
import json
import os

class WebsiteTestUser(HttpUser):
	wait_time = between(0.5, 20.0)
	host='http://127.0.0.1:8000'

	@task(1)
	def root(self):
		self.client.get("/")


	@task(2)
	def test_predict(self):
		self.client.post("/predict?data=sad&data=bad")