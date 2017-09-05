from tests.base import BaseTest


class TestDatabaseService(BaseTest):

    def setUp(self):
        super(TestDatabaseService, self).setUp()
        self.db = DatabaseService()


    def tearDown(self):
        super(TestDatabaseService, self).tearDown()


    def test_database_service_can_connect(self):
        self.assertIsNotNone(self.db)
