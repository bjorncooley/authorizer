from api import api
import json
from tests.base import BaseTest
from services.database_service import DatabaseService


class TestValidationToken(BaseTest):

    def setUp(self):
        super(TestValidationToken, self).setUp()
        self.app = api.app.test_client()


    def tearDown(self):
        super(TestValidationToken, self).tearDown()


    def test_create_validation_token_returns_200_with_valid_data(self):
        data = json.dumps({"email": "test@example.com"})
        result = self.app.post("/api/v1/validation-token/create", data=data)
        self.assertEqual(result.status_code, 200)


    def test_create_validation_token_returns_422_if_missing_data(self):
        result = self.app.post("/api/v1/validation-token/create")
        self.assertEqual(result.status_code, 422)


    def test_create_validation_token_returns_token(self):
        data = json.dumps({"email": "test@example.com"})
        result = self.app.post("/api/v1/validation-token/create", data=data)
        self.assertIsNotNone(json.loads(result.data)["token"])


    def test_confirm_validation_token_returns_401_with_invalid_data(self):
        result = self.app.get("/api/v1/validation-token/confirm?token=invalidtoken")
        self.assertEqual(result.status_code, 401)


    def test_confirm_validation_token_returns_422_if_missing_data(self):
        result = self.app.get("/api/v1/validation-token/confirm")
        self.assertEqual(result.status_code, 422)


    def test_confirm_validation_token_returns_correct_email_with_valid_data(self):
        email = "test@example.com"
        data = json.dumps({"email": email})
        result = self.app.post("/api/v1/validation-token/create", data=data)
        token = json.loads(result.data)["token"]

        result = self.app.get("/api/v1/validation-token/confirm?token=%s" % token)
        self.assertEqual(email, json.loads(result.data)["email"])
