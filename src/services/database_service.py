import sqlalchemy

from config.db.database_config import DatabaseConfig


class DatabaseService:

    def __init__(self):
        db_config = DatabaseConfig()
        self.conn = db_config.engine.connect()
        self.users = db_config.users


    def save_user(self, username, password):
        assert username != "", "Username must not be empty"
        assert password != "", "Password must not be empty"
        
        i = self.users.insert().values(
            username=username,
            password=password,
        )
        self.conn.execute(i)
