import json

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
        data = json.dumps({"email": "test@example.com", "password": "testpass"})
        response = self.app.post("/api/v1/create-user", data=data)
        self.assertEqual(200, response.status_code)


    def test_create_user_returns_422_with_missing_data(self):
        response = self.app.post("/api/v1/create-user")
        self.assertEqual(422, response.status_code)


    def test_create_user_returns_422_for_incorrectly_formatted_data(self):
        data = {"email": "test@example.com", "password": "testpass"}
        response = self.app.post("/api/v1/create-user", data=data)
        self.assertEqual(422, response.status_code)


    def test_create_user_returns_422_if_missing_email_or_password(self):
        data = json.dumps({"email": "test@example.com"})
        response = self.app.post("/api/v1/create-user", data=data)
        self.assertEqual(422, response.status_code)

        data = json.dumps({"password": "testpass"})
        response = self.app.post("/api/v1/create-user", data=data)
        self.assertEqual(422, response.status_code)


    def test_create_user_returns_422_if_email_or_password_are_empty(self):
        data = json.dumps({"email": "test@example.com", "password": ""})
        response = self.app.post("/api/v1/create-user", data=data)
        self.assertEqual(422, response.status_code)

        data = json.dumps({"email": "", "password": "testpass"})
        response = self.app.post("/api/v1/create-user", data=data)
        self.assertEqual(422, response.status_code)


    def test_create_user_returns_409_if_user_already_exists(self):
        data = json.dumps({"email": "test@example.com", "password": "testpass"})
        self.app.post("/api/v1/create-user", data=data)
        response = self.app.post("/api/v1/create-user", data=data)
        self.assertEqual(409, response.status_code)


    def test_create_user_saves_new_user_to_db(self):
        data = json.dumps({"email": "test@example.com", "password": "testpass"})
        self.app.post("/api/v1/create-user", data=data)

        query = "SELECT COUNT(*) FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertEqual(1, results[0][0])


    def test_create_user_creates_user_with_correct_email(self):
        email = "test@example.com"
        password = "testpass"

        data = json.dumps({"email": email, "password": password})
        self.app.post("/api/v1/create-user", data=data)

        query = "SELECT email, password FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertEqual(email, results[0][0])


    def test_create_user_creates_user_with_correct_first_and_last_name(self):
        email = "test@example.com"
        password = "testpass"
        first_name = "First"
        last_name = "Last"

        data = json.dumps({
            "email": email, 
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        })
        result = self.app.post("/api/v1/create-user", data=data)

        query = "SELECT first_name, last_name FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertEqual(first_name, results[0][0])
        self.assertEqual(last_name, results[0][1])


    def test_create_user_creates_user_as_applicant_by_default(self):
        email = "test@example.com"
        password = "testpass"

        data = json.dumps({"email": email, "password": password})
        self.app.post("/api/v1/create-user", data=data)

        query = "SELECT user_type FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertEqual("applicant", results[0][0])

