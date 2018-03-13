## Local setup

### Dependencies

This service uses pip to track and install dependencies. Instructions for installation are here: [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/)

It is recommended to set up a virtual environment before installing, documentation is here: [https://docs.python.org/3/tutorial/venv.html](https://docs.python.org/3/tutorial/venv.html) To use the start_dev script in this repository, the virtual environment must be named `authorizer`.

Once you have pip installed and your virtual environment activated (if desired), cd into the top-level project directory and run:
```
pip install -r requirements.txt
```


### Local database configuration

To configure, first get PostgreSQL installed and running on your local machine. To create a database, schema, and default admin user, cd into the top-level project directory and run:
```
psql -a -f config/db/setup_test_db.sql
```

If your local postgres installation requires a username and password, you will need to pass those in as arguments before the script name.

The best way to populate the local db is to get a db dump from the existing production instance:
```
pg_dump -U main_admin -d main -h main.cmmrjsgb2ell.us-west-1.rds.amazonaws.com | psql authorizer_test
```


## Running locally

Once the dependencies are installed, you have two options. Either set the required env variables and run flask manually, or run the start_dev.sh script. For the latter, simply run:
```
./dev/start_dev.sh
```

If you want to run the server manually, refer to the start_dev script for required env variables, then run:
```
export FLASK_APP=api/api.py
flask run
```


## Test Suite

There is a script to run the complete test suite. First, make sure your dependencies and local database are installed. Then activate your virtual environment and run:
```
./scripts/test.py
```

