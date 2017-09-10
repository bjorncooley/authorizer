import sqlalchemy
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from config.db.database_config import DatabaseConfig


class DatabaseService:

    def __init__(self):
        db_config = DatabaseConfig()
        self.conn = db_config.engine.connect()
        self.reset_tokens = db_config.reset_tokens
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


    def save_token(self, email, token):
        assert email != "", "email must not be empty"
        assert token != "", "token must not be empty"

        i = self.reset_tokens.insert().values(
            email=email,
            token=token,
        )
        result = self.conn.execute(i)


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


    def update_password(self, email, password):
        assert email != "", "email must not be empty"
        assert password != "", "Password must not be empty"

        hashed_password = generate_password_hash(password)

        u = self.users.update().where(
            self.users.c.email == email).values(
            password = hashed_password)
        self.conn.execute(u)


    def validate_token(self, token):
        assert token != "", "token must not be empty"

        q = select([self.reset_tokens.c.email]).where(
            self.reset_tokens.c.token == token)
        result = self.conn.execute(q)
        row = result.fetchone()

        if row is None:
            return None

        return row[0]

