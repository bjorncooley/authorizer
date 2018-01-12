import psycopg2

from tests.base import BaseTest
from services.database_service import DatabaseService
from werkzeug.security import check_password_hash


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


    def test_database_service_saves_email_as_lowercase(self):
        email = 'TEST@example.com'
        lowercaseEmail = 'test@example.com'
        password = 'testpass'
        self.db.save_user(
            email=email,
            password=password,
        )

        query = "SELECT email FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertEqual(lowercaseEmail, results[0][0])
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
        firstName = 'First'
        lastName = 'Last'
        self.db.save_user(
            email=email,
            password=password,
            firstName=firstName,
            lastName=lastName,
        )

        query = "SELECT first_name, last_name FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertEqual(firstName, results[0][0])
        self.assertEqual(lastName, results[0][1])
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
        userType = 'testtype'
        self.db.save_user(
            email=email,
            password=password,
            userType=userType,
        )

        result = self.db.authenticate_user(email=email, password=password)
        self.assertEqual(userType, result)


    def test_database_service_handles_nonexistent_user(self):
        email = 'test@example.com'
        password = 'testpass'
        result = self.db.authenticate_user(email=email, password=password)
        self.assertEqual(result, None)


    def test_database_service_creates_user_with_correct_user_type(self):
        email = 'test@example.com'
        password = 'testpass'
        userType = 'testtype'
        self.db.save_user(
            email=email,
            password=password,
            userType=userType,
        )

        query = "SELECT user_type FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertEqual(userType, results[0][0])
        curr.close()


    def test_database_service_can_return_user_data(self):
        email = 'test@example.com'
        password = 'testpass'
        userType = 'testtype'
        self.db.save_user(
            email=email,
            password=password,
            userType=userType,
        )

        user = self.db.get_user(email=email)
        self.assertIsNotNone(user)


    def test_database_service_returns_correct_user_data_on_get_user(self):
        email = 'test@example.com'
        password = 'testpass'
        userType = 'testtype'
        firstName = 'First'
        lastName = 'Last'
        self.db.save_user(
            email=email,
            password=password,
            userType=userType,
            firstName=firstName,
            lastName=lastName,
        )

        user = self.db.get_user(email=email)
        self.assertEqual(user['email'], email)
        self.assertEqual(user['firstName'], firstName)
        self.assertEqual(user['lastName'], lastName)
        self.assertEqual(user['userType'], userType)


    def test_database_service_can_save_reset_token(self):
        self.db.save_reset_token(
            email='test@example.com',
            token='thisisatesttoken',
        )

        query = "SELECT * FROM reset_tokens"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        curr.close()
        self.assertIsNotNone(results[0])


    def test_database_service_can_validate_saved_reset_token(self):
        email = 'test@example.com'
        token = 'testtoken'

        curr = self.conn.cursor()
        data = (email, token)
        query = "INSERT INTO reset_tokens (email, token) VALUES (%s, %s)"
        curr.execute(query, data)
        self.conn.commit()

        user_email = self.db.validate_reset_token(token=token)
        self.assertIsNotNone(user_email)


    def test_database_service_can_update_password(self):
        email = 'test@example.com'
        password1 = 'testpass1'
        password2 = 'testpass2'

        self.db.save_user(email=email, password=password1)
        query = "SELECT password FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        curr.close()
        first_password = results[0][0]

        self.db.update_password(email=email, password=password2)
        query = "SELECT password FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        curr.close()
        second_password = results[0][0]

        self.assertNotEqual(first_password, second_password)


    def test_database_service_can_save_cohort(self):
        email = 'test@example.com'
        cohort = 2
        self.db.save_user(email=email, password="testpass", cohort=cohort)
        query = "SELECT cohort FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        curr.close()
        savedCohort = results[0][0]
        self.assertEqual(savedCohort, cohort)


    def test_get_user_gets_cohort_for_student_users(self):
        email = 'test@example.com'
        cohort = 2
        self.db.save_user(email=email, password="testpass", cohort=cohort)
        user = self.db.get_user(email)
        self.assertEqual(user["cohort"], cohort)

