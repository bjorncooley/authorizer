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

        self.conn = psycopg2.connect(
            "dbname={0} user={1} password={2} host={3} port={4}".format(
            LOCAL_DBNAME, LOCAL_DBUSER, LOCAL_DBPASS, LOCAL_DBHOST, DBPORT
        ))


    def tearDown(self):
        super(TestDatabaseService, self).tearDown()
        query = "DELETE FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        self.conn.commit()


    def test_database_service_can_connect(self):
        self.assertIsNotNone(self.db)


    def test_database_service_can_save_user(self):
        username = 'testuser'
        password = 'testpass'
        self.db.save_user(
            username=username,
            password=password,
        )

        query = "SELECT COUNT(*) FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertEqual(1, results[0][0])
        curr.close()


    def test_database_service_saves_user_with_correct_username(self):
        username = 'testuser'
        password = 'testpass'
        self.db.save_user(
            username=username,
            password=password,
        )

        query = "SELECT username FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertEqual(username, results[0][0])
        curr.close()


    def test_database_service_saves_hashed_password(self):
        username = 'testuser'
        password = 'testpass'
        self.db.save_user(
            username=username,
            password=password,
        )

        query = "SELECT password FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertNotEqual(password, results[0][0])
        curr.close()


    def test_database_services_saves_correct_password(self):
        username = 'testuser'
        password = 'testpass'
        self.db.save_user(
            username=username,
            password=password,
        )

        query = "SELECT password FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertTrue(check_password_hash(results[0][0], password))
        curr.close()


    def test_database_service_saves_first_and_last_name(self):
        username = 'testuser'
        password = 'testpass'
        first_name = 'First'
        last_name = 'Last'
        self.db.save_user(
            username=username,
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
        username = 'testuser'
        password = 'testpass'
        self.db.save_user(
            username=username,
            password=password,
        )

        query = "SELECT first_name, last_name FROM users"
        curr = self.conn.cursor()
        curr.execute(query)
        results = curr.fetchall()
        self.assertEqual(None, results[0][0])
        self.assertEqual(None, results[0][1])
        curr.close()
