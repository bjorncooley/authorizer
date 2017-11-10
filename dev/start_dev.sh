#!/bin/bash
export WORKON_HOME="~/.virtualenvs"
export VIRTUALENVWRAPPER_PYTHON="/Library/Frameworks/Python.framework/Versions/3.6/bin/python3"
source /Library/Frameworks/Python.framework/Versions/3.6/bin/virtualenvwrapper.sh
workon authorizer
export FLASK_APP=src/api/api.py
flask run -p 4000
