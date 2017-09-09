
from api import api
from tests.base import BaseTest


class TestResetPassword(BaseTest):

    def setUp(self):
        super(TestResetPassword, self).setUp()
        self.app = api.app.test_client()



    def tearDown(self):
        super(TestResetPassword, self).tearDown()


    def test_reset_password_returns_200(self):
        result = self.app.post("/api/v1/reset-password")
        self.assertEqual(result.status_code, 200)


    def test_reset_password_returns_422_if_no_email(self):
        result = self.app.post("/api/v1/reset-password")
        self.assertEqual(result.status_code, 401)
