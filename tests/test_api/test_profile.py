from jose import jwt

from api import api
from config.api.api_config import APIConfig
from tests.base import BaseTest


class TestProfile(BaseTest):

    def setUp(self):
        super(TestProfile, self).setUp()
        self.app = api.app.test_client()

    
    def tearDown(self):
        super(TestProfile, self).tearDown()


    def post_request_with_token(self, endpoint):

        token = jwt.encode(
            {"subject": "test@example.com"},
            APIConfig().SECRET_KEY,
            algorithm="HS256",
        )
        result = self.app.post(
            endpoint,
            headers={"Authorization": "Bearer %s" % token},
        )
        return result


    def test_get_profile_returns_200(self):
        result = self.post_request_with_token("/api/v1/profile/get")
        self.assertEqual(200, result.status_code)


    def test_get_profile_returns_401_if_no_token(self):
        result = self.app.post("/api/v1/profile/get")
        self.assertEqual(401, result.status_code)
