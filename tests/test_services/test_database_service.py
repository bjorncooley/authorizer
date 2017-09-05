from tests.base import BaseTest
from services.database_service import DatabaseService

class TestDatabaseService(BaseTest):

    def setUp(self):
        super(TestDatabaseService, self).setUp()
        self.db = DatabaseService()


    def tearDown(self):
        super(TestDatabaseService, self).tearDown()


    def test_database_service_can_connect(self):
        self.assertIsNotNone(self.db)
