#!/bin/bash
export ENV=dev
export WORKON_HOME="~/.virtualenvs"
export VIRTUALENVWRAPPER_PYTHON='/usr/local/bin/python3'
source /usr/local/bin/virtualenvwrapper.sh
workon authorizer

export DBUSER=authorizer_admin
export DBPASS=default
export DBNAME=authorizer_test
export DBHOST=localhost

export FLASK_DEBUG=1
export FLASK_APP=api/api.py
export SECRET_KEY="notarealsecretkey"

flask run -p 4000
