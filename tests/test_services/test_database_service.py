import psycopg2

from tests.base import BaseTest
from services.database_service import DatabaseService

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
