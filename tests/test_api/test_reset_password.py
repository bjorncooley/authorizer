
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
        email = "test@example.com"
        token = "testtoken"

        db = DatabaseService()
        db.save_token(email=email, token=token)
        data = json.dumps({
            "token": token,
            "password": "testpass2",
            "passwordCheck": "testpass2",
        })
        result = self.app.post("/api/v1/reset-password", data=data)
        self.assertEqual(result.status_code, 200)


    def test_reset_password_returns_422_if_missing_params(self):
        result = self.app.post("/api/v1/reset-password")
        self.assertEqual(result.status_code, 422)


    def test_reset_password_returns_422_if_password_do_no_match(self):
        data = json.dumps({
            "token": "testtoken",
            "password": "testpass2",
            "passwordCheck": "testpass3",
        })
        result = self.app.post("/api/v1/reset-password", data=data)
        self.assertEqual(result.status_code, 422)


    def test_reset_password_returns_422_if_token_does_not_exist(self):
        data = json.dumps({
            "token": "testtoken",
            "password": "testpass2",
            "passwordCheck": "testpass2",
        })
        result = self.app.post("/api/v1/reset-password", data=data)
        self.assertEqual(result.status_code, 422)


    def test_reset_password_updates_password(self):
        email = "test@example.com"
        token = "testtoken"
        password1 = "testpassword1"
        password2 = "testpassword2"

        db = DatabaseService()
        db.save_user(email=email, password=password1)
        db.save_token(email=email, token=token)
        data = json.dumps({
            "token": token,
            "password": password2,
            "passwordCheck": password2,
        })

        self.app.post("/api/v1/reset-password", data=data)
        result = db.authenticate_user(email=email, password=password2)
        self.assertIsNotNone(result)

