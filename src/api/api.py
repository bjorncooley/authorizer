import logging
from pprint import pprint
import os
import random
import string
import sys
import uuid

from flask import (
    Flask,
    jsonify,
    make_response,
    request,
)
from flask_cors import CORS
import json
from jose import jwt
import requests
from sqlalchemy.exc import IntegrityError as SQLIntegrityError

SRC_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(SRC_DIR)
sys.path.insert(0, SRC_DIR)
sys.path.insert(0, BASE_DIR)

from lib.lib import (
    get_request_data,
    handle_error,
    send_reset_link,
)
from services.database_service import DatabaseService

app = Flask(__name__)
app.config.from_object("config.api.api_config.APIConfig")
CORS(app)
logger = logging.getLogger()


# Pull into separate lib
def check_params(request, required_fields):
    data = request.data
    missing_fields = []

    if not data:
        return make_response("Request parameters must not be empty", 422)

    try:
        parsedData = json.loads(data.decode('utf-8'))
    except TypeError:
        return make_response("Data must be convertible to JSON", 422)

    for field in required_fields:
        if field not in parsedData:
            missing_fields.append(field)
        elif len(parsedData[field]) == 0:
            missing_fields.append(field)

    if missing_fields:
        return make_response("The following fields are required: %r" % missing_fields, 422)

    return None


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
    try:
        db.save_user(
            email=email, 
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
        )
    except SQLIntegrityError:
        return make_response("User %s already exists" % data["email"], 409)

    return make_response("OK", 200)


@app.route("/api/v1/validation-token/confirm", methods=["GET"])
def confirm_validation_token():
    try:
        data = get_request_data(
            request,
            required_params=["token"],
        )
    except (ValueError, TypeError) as e:
        return handle_error(    
            message=str(e),
            logger=logger,
            status_code=422,
        )

    try:
        email = DatabaseService().confirm_validation_token(data["token"])
        if email is not None:
            return jsonify({"email": email})
    except TypeError:
        logger.error("Could not get email for token %s" % data["token"])

    return make_response("Invalid token", 401)


@app.route("/api/v1/validation-token/create", methods=["POST"])
def create_validation_token():
    try:
        data = get_request_data(
            request,
            required_params=["email"],
        )
    except (ValueError, TypeError) as e:
        return handle_error(    
            message=str(e),
            logger=logger,
            status_code=422,
        )

    token = DatabaseService().create_validation_token(email=data["email"])
    if token is None:
        return make_response("Could not generate unique token", 500)
        
    return jsonify({"token": token})


@app.route("/api/v1/profile/get", methods=["GET"])
def get_profile():

    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return make_response("Valid token required", 401)

    try:
        encoded = auth_header.split(" ")[1]
        decoded = jwt.decode(
            encoded, 
            app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )
        email = decoded["subject"]
    except:
        return make_response("Invalid token", 401)

    db = DatabaseService()
    user = db.get_user(email)
    formattedUser = {
        "email": user["email"],
        "firstName": user["first_name"],
        "lastName": user["last_name"],
        "userType": user["user_type"],
    }
    return jsonify(formattedUser)


@app.route("/api/v1/health-check", methods=["GET"])
def health_check():
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
    user_type = db.authenticate_user(email=email, password=password)
    if not user_type:
        return make_response("Error: invalid credentials", 401)

    token = jwt.encode(
        {"subject": email, "user_type": user_type},
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    return jsonify({"token": token})


@app.route("/api/v1/forgot-password", methods=["POST"])
def forgot_password():

    try:
        data = get_request_data(
            request,
            required_params=["email", "resetURL"],
        )
    except (ValueError, TypeError) as e:
        return handle_error(    
            message=str(e),
            logger=logger,
            status_code=422,
        )

    token = uuid.uuid4().hex
    mailgun_response = send_reset_link(
        email=data["email"],
        token=token,
        url=data["resetURL"],
    )
    if mailgun_response.status_code != 200:
        return make_response(
            '''There was an error sending your reset link,
            please email tech@missionu.com with this error: %s'''
            % mailgun_response.text, mailgun_response.status_code)

    db = DatabaseService()
    db.save_reset_token(
        email=data["email"], 
        token=token,
    )
    return make_response("OK", 200)


@app.route("/api/v1/reset-password", methods=["POST"])
def reset_password():
    error = check_params(request, ["token", "password", "passwordCheck"])
    if error:
        return error

    data = json.loads(request.data.decode('utf-8'))
    token = data["token"]
    password = data["password"]
    password_check = data["passwordCheck"]

    if password != password_check:
        return make_response("Passwords do not match", 422)

    db = DatabaseService()
    user_email = db.validate_reset_token(token=token)
    if not user_email:
        return make_response("Invalid token", 422)

    db.update_password(email=user_email, password=password)

    return make_response("OK", 200)

