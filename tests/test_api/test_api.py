from tests.base import BaseTest
from api import api

class TestAPI(BaseTest):

    def setUp(self):
        super(TestAPI, self).setUp()
        self.app = api.app.test_client()

    def tearDown(self):
        super(TestAPI, self).tearDown()

    def test_healthcheck_returns_200(self):
        response = self.app.get("/health-check")
        self.assertEqual(200, response.status_code)
