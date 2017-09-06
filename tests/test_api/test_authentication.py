import json

from services.database_service import DatabaseService
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


    def test_login_returns_422_if_username_or_password_are_empty(self):
        data = json.dumps({"username": "testuser", "password": ""})
        result = self.app.post("/api/v1/login", data=data)
        self.assertEqual(result.status_code, 422)

        data = json.dumps({"username": "", "password": "testpass"})
        result = self.app.post("/api/v1/login", data=data)
        self.assertEqual(result.status_code, 422)


    def test_login_returns_200_with_error_message_if_invalid_credentials(self):
        db = DatabaseService()
        username = "testuser"
        password = "testpass"
        db.save_user(username=username, password=password)

        data = json.dumps({"username": username, "password": password})
        result = self.app.post("/api/v1/login", data=data)
        self.assertEqual(result.status_code, 422)
        self.assertContains(result.text, "Error")
