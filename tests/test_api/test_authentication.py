import json
from jose import jwt

from config.api.api_config import APIConfig
from services.database_service import DatabaseService
from tests.base import BaseTest
from api import api

class TestAPI(BaseTest):

    def setUp(self):
        super(TestAPI, self).setUp()
        self.app = api.app.test_client()

    
    def tearDown(self):
        super(TestAPI, self).tearDown()


    def test_login_returns_200_with_valid_credentials(self):
        email = "test@example.com"
        password = "testpass"
        db = DatabaseService()
        db.save_user(email=email, password=password)
        data = json.dumps({"email": "test@example.com", "password": "testpass"})
        result = self.app.post("/api/v1/login", data=data)
        self.assertEqual(result.status_code, 200)


    def test_login_returns_jwt_token_for_valid_credentials(self):
        email = "test@example.com"
        password = "testpass"
        db = DatabaseService()
        api_config = APIConfig()
        db.save_user(email=email, password=password)
        data = json.dumps({"email": "test@example.com", "password": "testpass"})

        result = self.app.post("/api/v1/login", data=data)
        try:
            data = json.loads(result.data)
            decoded = jwt.decode(data, api_config.SECRET_KEY, algorithms=["HS256"])
        except:
            decoded = None
        self.assertIsNotNone(decoded)


    def test_jwt_token_contains_subject_and_user_type(self):
        email = "test@example.com"
        password = "testpass"
        db = DatabaseService()
        api_config = APIConfig()
        db.save_user(email=email, password=password)
        data = json.dumps({"email": "test@example.com", "password": "testpass"})

        result = self.app.post("/api/v1/login", data=data)
        try:
            data = json.loads(result.data)
            decoded = jwt.decode(data, api_config.SECRET_KEY, algorithms=["HS256"])
            subject = decoded["subject"]
            user_type = decoded["user_type"]
        except:
            decoded = None
        self.assertIsNotNone(decoded)


    def test_login_returns_422_if_no_data(self):
        result = self.app.post("/api/v1/login")
        self.assertEqual(result.status_code, 422)


    def test_login_returns_422_if_data_formatted_incorrectly(self):
        data = {"email": "test@example.com", "password": "testpass"}
        result = self.app.post("/api/v1/login", data=data)
        self.assertEqual(result.status_code, 422)


    def test_login_returns_422_if_missing_email_or_password(self):
        data = json.dumps({"email": "test@example.com"})
        result = self.app.post("/api/v1/login", data=data)
        self.assertEqual(result.status_code, 422)

        data = json.dumps({"password": "testpass"})
        result = self.app.post("/api/v1/login", data=data)
        self.assertEqual(result.status_code, 422)


    def test_login_returns_422_if_email_or_password_are_empty(self):
        data = json.dumps({"email": "test@example.com", "password": ""})
        result = self.app.post("/api/v1/login", data=data)
        self.assertEqual(result.status_code, 422)

        data = json.dumps({"email": "", "password": "testpass"})
        result = self.app.post("/api/v1/login", data=data)
        self.assertEqual(result.status_code, 422)


    def test_login_returns_401_with_invalid_credentials(self):
        db = DatabaseService()
        email = "test@example.com"
        password = "testpass"
        db.save_user(email=email, password=password)

        data = json.dumps({"email": email, "password": "wrongpassword"})
        result = self.app.post("/api/v1/login", data=data)
        self.assertEqual(result.status_code, 401)
