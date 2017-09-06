from nose.tools import nottest
import psycopg2
import unittest

from config.db.database_config import (
    LOCAL_DBUSER,
    LOCAL_DBPASS,
    LOCAL_DBNAME,
    LOCAL_DBHOST,
)

DBUSER = LOCAL_DBUSER
DBPASS = LOCAL_DBPASS
DBHOST = LOCAL_DBHOST
DBNAME = LOCAL_DBNAME
DBPORT = "5432"


class BaseTest(unittest.TestCase):

    @nottest
    def connect_db(self, dbname, dbuser, dbpass, dbhost, dbport):
        conn = psycopg2.connect("dbname={0} user={1} password={2} host={3} port={4}".format(dbname, dbuser, dbpass, dbhost, dbport))
        return conn

    def setUp(self):
        self.conn = self.connect_db(DBNAME, DBUSER, DBPASS, DBHOST, DBPORT)

    def tearDown(self):
        curr = self.conn.cursor()
        query = "DELETE FROM users"
        curr.execute(query)
        self.conn.commit()
