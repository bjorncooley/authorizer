import sqlalchemy
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from config.db.database_config import DatabaseConfig


class DatabaseService:

    def __init__(self):
        db_config = DatabaseConfig()
        self.conn = db_config.engine.connect()
        self.users = db_config.users


    def save_user(self, email, password, user_type=None, first_name=None, last_name=None):
        assert email != "", "email must not be empty"
        assert password != "", "Password must not be empty"

        # set default user_type to student
        if user_type is None:
            user_type = "student"

        hashedPassword = generate_password_hash(password)

        i = self.users.insert().values(
            email=email,
            password=hashedPassword,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
        )
        self.conn.execute(i)


    def authenticate_user(self, email, password):
        assert email != "", "email must not be empty"
        assert password != "", "Password must not be empty"

        q = select([self.users.c.password]).where(
            self.users.c.email == email
        )
        result = self.conn.execute(q)
        row = result.fetchone()
        if not row:
            return False
        return check_password_hash(row[0], password)
