from flask import (
    Flask,
    make_response,
    request,
)
import json
import os
import sys

SRC_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)
sys.path.insert(0, SRC_DIR)
sys.path.insert(0, ROOT_DIR)

from services.database_service import DatabaseService

app = Flask(__name__)


@app.route("/api/v1/health-check", methods=["GET"])
def health_check():
    return make_response("OK", 200)


@app.route("/api/v1/create-user", methods=["POST"])
def create_user():
    data = request.data
    if not data:
        return make_response("Request parameters must not be empty", 422)

    try:
        parsedData = json.loads(data)
    except TypeError:
        return make_response("Data must be convertible to JSON", 422)

    try:
        username = parsedData["username"]
        password = parsedData["password"]
    except KeyError:
        return make_response("Username and password are required parameters", 422)

    if len(username) == 0 or len(password) == 0:
        return make_response("Username and password cannot be blank", 422)

    first_name = None
    last_name = None
    if "first_name" in parsedData:
        first_name = parsedData["first_name"]
    if "last_name" in parsedData:
        last_name = parsedData["last_name"]

    db = DatabaseService()
    db.save_user(
        username=username, 
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

    return make_response("OK", 200)


@app.route("/api/v1/login", methods=["POST"])
def login():
    data = request.data
    if not data:
        return make_response("Request parameters must not be empty", 422)

    return make_response("OK", 200)

