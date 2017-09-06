import json

from tests.base import BaseTest
from api import api

class TestAPI(BaseTest):

    def setUp(self):
        super(TestAPI, self).setUp()
        self.app = api.app.test_client()

    
    def tearDown(self):
        super(TestAPI, self).tearDown()


    def test_login_returns_200(self):
        data = json.dumps({"username": "testuser", "password": "testpass"})
        result = self.app.post("/api/v1/login", data=data)
        self.assertEqual(result.status_code, 200)


    def test_login_returns_422_if_no_data(self):
        result = self.app.post("/api/v1/login")
        self.assertEqual(result.status_code, 422)


    def test_login_returns_422_if_data_formatted_incorrectly(self):
        data = {"username": "testuser", "password": "testpass"}
        result = self.app.post("/api/v1/login", data=data)
        self.assertEqual(result.status_code, 422)


    def test_login_returns_422_if_missing_username_or_password(self):
        data = json.dumps({"username": "testuser"})
        result = self.app.post("/api/v1/login", data=data)
        self.assertEqual(result.status_code, 422)

        data = json.dumps({"password": "testpass"})
        result = self.app.post("/api/v1/login", data=data)
        self.assertEqual(result.status_code, 422)
