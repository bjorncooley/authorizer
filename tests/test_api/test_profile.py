from jose import jwt
import json

from api import api
from config.api.api_config import APIConfig
from tests.base import BaseTest
from services.database_service import DatabaseService


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


    def test_get_profile_returns_user_data(self):
        db = DatabaseService()
        email = "test@example.com"
        password = "testpass"
        first_name = "First"
        last_name = "Last"
        user_type = "testtype"

        db.save_user(
            email=email,
            password=password,
            user_type=user_type,
            first_name=first_name,
            last_name=last_name,
        )

        result = self.post_request_with_token("/api/v1/profile/get")
        data = json.loads(result.data)
        self.assertEqual(data["email"], email)
        self.assertEqual(data["user_type"], user_type)
        self.assertEqual(data["first_name"], first_name)
        self.assertEqual(data["last_name"], last_name)

