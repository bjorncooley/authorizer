from config.database_config import DatabaseConfig


class DatabaseService:

    def __init__(self):
        db_config = DatabaseConfig()
        self.conn = db_config.engine.connect()
