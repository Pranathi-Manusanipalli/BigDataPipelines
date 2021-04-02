from locust import HttpUser, task, between
from starlette.testclient import TestClient
import json

class WebsiteTestUser(HttpUser):
	wait_time = between(0.5, 20.0)
	host='http://127.0.0.1:8000'
	@task(1)
	def root(self):
		self.client.get("/")

	@task(2)
	def test_cycles(self):
		for item_id in range(1,4):
			self.client.get("/cycles?unit_number={}&fault=FD001".format(item_id), name="/cycles")


	@task(3)
	def test_rul(self):
		for item_id in range(1,3):
			self.client.get("/rul?unit_number={}&fault=FD001".format(item_id), name="/rul")

	@task(4)
	def test_operational_data(self):
		for item_id in range(1,3):
			self.client.get("/engine/operational_data?unit_number={}&dataset_type=train&fault=FD001".format(item_id), name="/operation")

	@task(5)
	def test_sensor_data(self):
		for item_id in range(1,3):
			self.client.get("/engine/sensordata?unit_number={}&dataset_type=train&fault=FD001".format(item_id), name="/sensor")

