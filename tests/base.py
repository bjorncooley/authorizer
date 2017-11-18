from nose.tools import nottest
import os
import psycopg2
import unittest

from config.api.api_config import (
    SANDBOX_MAILGUN_KEY,
    SANDBOX_MAILGUN_URL,
)
from config.db.database_config import (
    LOCAL_DBUSER,
    LOCAL_DBPASS,
    LOCAL_DBNAME,
    LOCAL_DBHOST,
)
from tests.test_api.mock_server import MockServer


DBUSER = LOCAL_DBUSER
DBPASS = LOCAL_DBPASS
DBHOST = LOCAL_DBHOST
DBNAME = LOCAL_DBNAME
DBPORT = "5432"


class BaseTest(unittest.TestCase):

    @nottest
    def connect_db(self, dbname, dbuser, dbpass, dbhost, dbport):
        if os.getenv("CIRCLECI"):
            dbname = "circle_test"
            dbuser = "ubuntu"
            dbpass = ""
            dbhost = "127.0.0.1"

        conn = psycopg2.connect("dbname={0} user={1} password={2} host={3} port={4}".format(dbname, dbuser, dbpass, dbhost, dbport))
        return conn


    def setUp(self):
        self.conn = self.connect_db(DBNAME, DBUSER, DBPASS, DBHOST, DBPORT)
        self.server = MockServer(port=1234)
        self.server.start()
        os.environ["EMAIL_ENDPOINT"] = self.server.url + "/mailgun"


    def tearDown(self):
        self.server.shutdown_server()
        curr = self.conn.cursor()
        query = "DELETE FROM users"
        curr.execute(query)
        query = "DELETE FROM reset_tokens"
        curr.execute(query)
        query = "DELETE FROM validation_tokens"
        curr.execute(query)
        self.conn.commit()
        self.conn.close()
