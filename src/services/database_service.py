import random
import sqlalchemy
from sqlalchemy import select
import string
import uuid
from werkzeug.security import check_password_hash, generate_password_hash

from config.db.database_config import DatabaseConfig


class DatabaseService:

    def __init__(self):
        db_config = DatabaseConfig()
        self.conn = db_config.engine.connect()
        self.reset_tokens = db_config.reset_tokens
        self.validation_tokens = db_config.validation_tokens
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


    def create_validation_token(self, email):
        assert email != "", "email must not be empty"

        # Try to generate unique token up to 3 times. Assume that if cannot
        # generate unique token on the 3rd round something is broken,
        # return nil
        for i in range(3):
            token = uuid.uuid4().hex

            try:
                self.conn.execute(self.validation_tokens.insert().values(
                    email=email,
                    token=token,
                ))
                break
            except sqlalchemy.exc.IntegrityError:
                token = None

        return token


    def confirm_validation_token(self, token):
        assert token != "", "token must not be empty"

        q = select([self.validation_tokens.c.email]).where(
            self.validation_tokens.c.token == token
        )
        return self.conn.execute(q).fetchone()[0]


    def get_user(self, email):
        assert email != "", "email must not be empty"

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
            user["first_name"] = row[0]
            user["last_name"] = row[1]
            user["user_type"] = row[2]
            user["email"] = email
        return user


    def save_reset_token(self, email, token):
        assert email != "", "email must not be empty"
        assert token != "", "token must not be empty"

        i = self.reset_tokens.insert().values(
            email=email,
            token=token,
        )
        self.conn.execute(i)


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


    def validate_reset_token(self, token):
        assert token != "", "token must not be empty"

        q = select([self.reset_tokens.c.email]).where(
            self.reset_tokens.c.token == token)
        result = self.conn.execute(q)
        row = result.fetchone()

        if row is None:
            return None

        return row[0]

