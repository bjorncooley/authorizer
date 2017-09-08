import sqlalchemy
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from config.db.database_config import DatabaseConfig


class DatabaseService:

    def __init__(self):
        db_config = DatabaseConfig()
        self.conn = db_config.engine.connect()
        self.users = db_config.users


    def authenticate_user(self, email, password):
        assert email != "", "email must not be empty"
        assert password != "", "Password must not be empty"

        q = select([self.users.c.password, self.users.c.user_type]).where(
            self.users.c.email == email
        )
        result = self.conn.execute(q)
        row = result.fetchone()
        if not row:
            return None

        # If the password is correct, return the user_type
        if check_password_hash(row[0], password):
            return row[1]
        else:
            return None


    def get_user(self, email):
        assert email != "", "email must not be empty"

        print("EMAIL IS %r" % email)
        q = select([
            self.users.c.first_name,
            self.users.c.last_name,
            self.users.c.user_type]
        ).where(self.users.c.email == email)

        result = self.conn.execute(q)
        row = result.fetchone()

        user = None
        if row is not None:
            user = {}
            user['first_name'] = row[0]
            user['last_name'] = row[1]
            user['user_type'] = row[2]
            user['email'] = email
        print("RESULT IS %r" % row)
        return user


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
        result = self.conn.execute(i)
