import datetime
import os
import sqlalchemy
from sqlalchemy import (
    Column,
    create_engine,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
)

LOCAL_DBUSER = "authorizer_admin"
LOCAL_DBPASS = "default"
LOCAL_DBNAME = "authorizer_test"
LOCAL_DBHOST = "localhost"


class DatabaseConfig:

    def __init__(self):
        # Get credentials from environment or load defaults
        dbuser = os.getenv("DBUSER", LOCAL_DBUSER)
        dbpass = os.getenv("DBPASS", LOCAL_DBPASS)
        dbname = os.getenv("DBNAME", LOCAL_DBNAME)
        dbhost = os.getenv("DBHOST", LOCAL_DBHOST)

        # DB connection
        connection_string = "postgresql+psycopg2://{0}:{1}@{2}/{3}".format(
            dbuser,
            dbpass,
            dbhost,
            dbname
        )
        self.engine = create_engine(connection_string)
        self.metadata = MetaData()

        self.users = Table('users', self.metadata,
            Column('cohort', Integer),
            Column('first_name', String),
            Column('id', Integer, primary_key=True),
            Column('last_name', String),
            Column('password', String),
            Column('salesforce_id', String),
            Column('salt', String),
            Column('email', String),
            Column('user_type', String),
        )

        self.reset_tokens = Table('reset_tokens', self.metadata,
            Column('email', String),
            Column('id', Integer, primary_key=True),
            Column('time_created', DateTime(timezone=True), onupdate=datetime.datetime.now),
            Column('token', String),
        )

        self.validation_tokens = Table('validation_tokens', self.metadata,
            Column('email', String),
            Column('id', Integer, primary_key=True),
            Column('time_created', DateTime(timezone=True), onupdate=datetime.datetime.now),
            Column('token', String),
        )

    def create_tables(self):
        self.metadata.create_all(self.engine)
