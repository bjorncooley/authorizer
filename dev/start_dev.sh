#!/bin/bash
export ENV=dev
export WORKON_HOME="~/.virtualenvs"
export VIRTUALENVWRAPPER_PYTHON='/usr/local/bin/python3'
source /usr/local/bin/virtualenvwrapper.sh
workon authorizer

export DBUSER=local_admin
export DBPASS=default
export DBNAME=missionu_main_dev
export DBHOST=localhost
export FLASK_APP=api/api.py
export SECRET_KEY="notarealsecretkey"

flask run -p 4000
