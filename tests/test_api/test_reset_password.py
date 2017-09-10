
from api import api
import json
from tests.base import BaseTest


class TestResetPassword(BaseTest):

    def setUp(self):
        super(TestResetPassword, self).setUp()
        self.app = api.app.test_client()


    def tearDown(self):
        super(TestResetPassword, self).tearDown()


    def test_forgot_password_returns_200(self):
        data = json.dumps({"email": "test@example.com"})
        result = self.app.post("/api/v1/forgot-password", data=data)
        self.assertEqual(result.status_code, 200)


    def test_forgot_password_returns_422_if_no_email(self):
        result = self.app.post("/api/v1/forgot-password")
        self.assertEqual(result.status_code, 422)


    def test_forgot_password_creates_new_forgot_token(self):
        data = json.dumps({"email": "test@example.com"})
        self.app.post("/api/v1/forgot-password", data=data)

        query = "SELECT token FROM reset_tokens"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertIsNotNone(results[0][0])


    def test_reset_password_returns_200(self):
        result = self.app.post("/api/v1/reset-password")
        self.assertEqual(result.status_code, 200)
