## Local setup

### Local database configuration

To configure, first get PostgreSQL installed and running on your local machine. To create a database, schema, and default admin user, cd into the top-level project directory and run:
```
psql -a -f config/db/setup_test_db.sql
```

If your local postgres installation requires a username and password, you will need to pass those in as arguments before the script name.

To populate the local database with the correct schema, run:
```
python config/db/create_tables.py
```

