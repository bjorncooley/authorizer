import psycopg2

from tests.base import BaseTest
from services.database_service import DatabaseService
from werkzeug.security import check_password_hash

from config.db.database_config import (
    LOCAL_DBUSER,
    LOCAL_DBPASS,
    LOCAL_DBHOST,
    LOCAL_DBNAME
)
DBPORT = "5432"

class TestDatabaseService(BaseTest):

    def setUp(self):
        super(TestDatabaseService, self).setUp()
        self.db = DatabaseService()


    def tearDown(self):
        super(TestDatabaseService, self).tearDown()


    def test_database_service_can_connect(self):
        self.assertIsNotNone(self.db)


    def test_database_service_can_save_user(self):
        email = 'test@example.com'
        password = 'testpass'
        self.db.save_user(
            email=email,
            password=password,
        )

        query = "SELECT COUNT(*) FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertEqual(1, results[0][0])
        curr.close()


    def test_database_service_saves_user_with_correct_email(self):
        email = 'test@example.com'
        password = 'testpass'
        self.db.save_user(
            email=email,
            password=password,
        )

        query = "SELECT email FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertEqual(email, results[0][0])
        curr.close()


    def test_database_service_saves_hashed_password(self):
        email = 'test@example.com'
        password = 'testpass'
        self.db.save_user(
            email=email,
            password=password,
        )

        query = "SELECT password FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertNotEqual(password, results[0][0])
        curr.close()


    def test_database_services_saves_correct_password(self):
        email = 'test@example.com'
        password = 'testpass'
        self.db.save_user(
            email=email,
            password=password,
        )

        query = "SELECT password FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertTrue(check_password_hash(results[0][0], password))
        curr.close()


    def test_database_service_saves_first_and_last_name(self):
        email = 'test@example.com'
        password = 'testpass'
        first_name = 'First'
        last_name = 'Last'
        self.db.save_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        query = "SELECT first_name, last_name FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertEqual(first_name, results[0][0])
        self.assertEqual(last_name, results[0][1])
        curr.close()


    def test_database_service_handles_default_values_for_first_and_last_name(self):
        email = 'test@example.com'
        password = 'testpass'
        self.db.save_user(
            email=email,
            password=password,
        )

        query = "SELECT first_name, last_name FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertEqual(None, results[0][0])
        self.assertEqual(None, results[0][1])
        curr.close()


    def test_database_service_can_authorize_valid_user_credentials(self):
        email = 'test@example.com'
        password = 'testpass'
        self.db.save_user(
            email=email,
            password=password,
        )

        result = self.db.authenticate_user(email=email, password=password)
        self.assertIsNotNone(result)


    def test_database_service_returns_user_type_after_authorizing(self):
        email = 'test@example.com'
        password = 'testpass'
        user_type = 'testtype'
        self.db.save_user(
            email=email,
            password=password,
            user_type=user_type,
        )

        result = self.db.authenticate_user(email=email, password=password)
        self.assertEqual(user_type, result)


    def test_database_service_handles_nonexistent_user(self):
        email = 'test@example.com'
        password = 'testpass'
        result = self.db.authenticate_user(email=email, password=password)
        self.assertEqual(result, None)


    def test_database_service_creates_user_with_correct_user_type(self):
        email = 'test@example.com'
        password = 'testpass'
        user_type = 'testtype'
        self.db.save_user(
            email=email,
            password=password,
            user_type=user_type,
        )

        query = "SELECT user_type FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertEqual(user_type, results[0][0])
        curr.close()


    def test_database_service_can_return_user_data(self):
        email = 'test@example.com'
        password = 'testpass'
        user_type = 'testtype'
        self.db.save_user(
            email=email,
            password=password,
            user_type=user_type,
        )

        user = self.db.get_user(email=email)
        self.assertIsNotNone(user)


    def test_database_service_returns_correct_user_data(self):
        email = 'test@example.com'
        password = 'testpass'
        user_type = 'testtype'
        first_name = 'First'
        last_name = 'Last'
        self.db.save_user(
            email=email,
            password=password,
            user_type=user_type,
            first_name=first_name,
            last_name=last_name,
        )

        user = self.db.get_user(email=email)
        self.assertEqual(user['email'], email)
        self.assertEqual(user['first_name'], first_name)
        self.assertEqual(user['last_name'], last_name)
        self.assertEqual(user['user_type'], user_type)


    def test_database_service_can_save_reset_token(self):
        self.db.save_token(
            email='test@example.com',
            token='thisisatesttoken',
        )

        query = "SELECT * FROM reset_tokens"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        curr.close()
        self.assertIsNotNone(results[0])

