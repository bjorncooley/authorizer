from tests.base import BaseTest
from api import api

class TestAPI(BaseTest):

    def setUp(self):
        super(TestAPI, self).setUp()
        self.app = api.app.test_client()

    
    def tearDown(self):
        super(TestAPI, self).tearDown()


    def test_login_returns_200(self):
        result = self.app.post("/api/v1/login")
        self.assertEqual(result.status_code, 200)


    def test_login_returns_422_if_no_data(self):
        result = self.app.post("/api/v1/login")
        self.assertEqual(result.status_code, 422)
