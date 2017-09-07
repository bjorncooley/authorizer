from flask import (
    Flask,
    jsonify,
    make_response,
    request,
)
import json
from jose import jwt
import logging
import os
import sys

SRC_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(SRC_DIR)
sys.path.insert(0, SRC_DIR)
sys.path.insert(0, BASE_DIR)

from services.database_service import DatabaseService

app = Flask(__name__)
app.config.from_object("config.api.api_config.APIConfig")
logger = logging.getLogger()


# Pull into separate lib
def check_params(request, required_fields):
    data = request.data
    missing_fields = []

    if not data:
        return make_response("Request parameters must not be empty", 422)

    json.loads(data.decode('utf-8'))
    try:
        parsedData = json.loads(data)
    except TypeError:
        logger.info("Error converting data to JSON: %r" % data)
        return make_response("Data must be convertible to JSON", 422)

    for field in required_fields:
        if field not in parsedData:
            missing_fields.append(field)
        elif len(parsedData[field]) == 0:
            missing_fields.append(field)

    if missing_fields:
        return make_response("The following fields are required: %r" % missing_fields, 422)

    return None


@app.route("/api/v1/health-check", methods=["GET"])
def health_check():
    return make_response("OK", 200)


@app.route("/api/v1/create-user", methods=["POST"])
def create_user():
    
    error = check_params(request, ["email", "password"])
    if error:
        return error

    data = json.loads(request.data.decode('utf-8'))
    email = data["email"]
    password = data["password"]
    first_name = None
    last_name = None
    user_type = None

    if "first_name" in data:
        first_name = data["first_name"]
    if "last_name" in data:
        last_name = data["last_name"]
    if "user_type" in data:
        user_type = data["user_type"]

    db = DatabaseService()
    db.save_user(
        email=email, 
        password=password,
        first_name=first_name,
        last_name=last_name,
        user_type=user_type,
    )

    return make_response("OK", 200)


@app.route("/api/v1/login", methods=["POST"])
def login():
    error = check_params(request, ["email", "password"])
    if error:
        return error

    data = json.loads(request.data.decode('utf-8'))
    email = data["email"]
    password = data["password"]

    db = DatabaseService()
    authenticated = db.authenticate_user(email=email, password=password)
    if not authenticated:
        return make_response("Error: invalid credentials", 401)

    token = jwt.encode(
        {"subject": email},
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    return jsonify(token)

