from tests.base import BaseTest
from api import api

class TestAPI(BaseTest):

    def setUp(self):
        super(TestAPI, self).setUp()
        self.app = api.app.test_client()


    def tearDown(self):
        super(TestAPI, self).tearDown()


    def test_health_check_returns_200(self):
        response = self.app.get("/api/v1/health-check")
        self.assertEqual(200, response.status_code)


    def test_create_user_returns_200(self):
        response = self.app.post("/api/v1/create-user")
        self.assertEqual(200, response.status_code)


    def test_create_user_returns_422_with_missing_data(self):
        response = self.app.post("/api/v1/create-user")
        self.assertEqual(422, response.status_code)
