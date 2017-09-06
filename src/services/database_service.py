import sqlalchemy
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from config.db.database_config import DatabaseConfig


class DatabaseService:

    def __init__(self):
        db_config = DatabaseConfig()
        self.conn = db_config.engine.connect()
        self.users = db_config.users


    def save_user(self, username, password, first_name=None, last_name=None):
        assert username != "", "Username must not be empty"
        assert password != "", "Password must not be empty"

        hashedPassword = generate_password_hash(password)

        i = self.users.insert().values(
            username=username,
            password=hashedPassword,
            first_name=first_name,
            last_name=last_name,
        )
        self.conn.execute(i)


    def authenticate_user(self, username, password):
        assert username != "", "Username must not be empty"
        assert password != "", "Password must not be empty"

        q = select([self.users.c.password]).where(
            self.users.c.username == username
        )
        result = self.conn.execute(q)
        row = result.fetchone()
        if not row:
            return False
        return check_password_hash(row[0], password)
