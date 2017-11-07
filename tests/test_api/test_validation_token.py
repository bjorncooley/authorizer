from api import api
import json
from tests.base import BaseTest
from services.database_service import DatabaseService


class TestResetPassword(BaseTest):

    def setUp(self):
        super(TestResetPassword, self).setUp()
        self.app = api.app.test_client()


    def tearDown(self):
        super(TestResetPassword, self).tearDown()


    def test_create_validation_token_returns_200_with_valid_data(self):
        data = json.dumps({"email": "test@example.com"})
        result = self.app.post("/api/v1/validation-token/create", data=data)
        self.assertEqual(result.status_code, 200)


    def test_create_validation_token_returns_422_if_missing_data(self):
        result = self.app.post("/api/v1/validation-token/create")
        self.assertEqual(result.status_code, 422)

