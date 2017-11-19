#!/bin/bash
export WORKON_HOME="~/.virtualenvs"
export VIRTUALENVWRAPPER_PYTHON='/usr/local/bin/python3'
source /usr/local/bin/virtualenvwrapper.sh
workon authorizer
export FLASK_APP=api/api.py
flask run -p 4000
