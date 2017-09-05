import os
import sqlalchemy
from sqlalchemy import (
    create_engine,
    MetaData,
)

LOCAL_DBUSER = "local_admin"
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
