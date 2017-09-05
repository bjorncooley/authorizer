import sqlalchemy

from config.db.database_config import DatabaseConfig


class DatabaseService:

    def __init__(self):
        db_config = DatabaseConfig()
        self.conn = db_config.engine.connect()
        self.users = db_config.users


    def save_user(self, username, password):
        i = self.users.insert().values(
            username=username,
            password=password,
        )
        self.conn.execute(i)
