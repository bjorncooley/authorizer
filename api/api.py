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

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
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

    try:
        data = get_request_data(
            request,
            required_params=["email", "password"],
        )
    except (ValueError, TypeError) as e:
        return handle_error("%s: %s" % (request.url, str(e)), 422)
    
    email = data["email"]
    password = data["password"]
    cohort = data.get("cohort", None)
    firstName = data.get("firstName", None)
    lastName = data.get("lastName", None)
    userType = data.get("userType", None)

    db = DatabaseService()
    try:
        db.save_user(
            email=email, 
            password=password,
            cohort=cohort,
            firstName=firstName,
            lastName=lastName,
            userType=userType,
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
        return handle_error("%s: %s" % (request.url, str(e)), 422)

    try:
        email = DatabaseService().confirm_validation_token(data["token"])
        if email is not None:
            return jsonify({"email": email})
    except TypeError:
        handle_error("Could not get email for token %s" % data["token"], 422)

    return make_response("Invalid token", 401)


@app.route("/api/v1/validation-token/create", methods=["POST"])
def create_validation_token():
    try:
        data = get_request_data(
            request,
            required_params=["email"],
        )
    except (ValueError, TypeError) as e:
        return handle_error("%s: %s" % (request.url, str(e)), 422)

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
        "firstName": user["firstName"],
        "lastName": user["lastName"],
        "userType": user["userType"],
    }
    return jsonify(formattedUser)


@app.route("/api/v1/health-check", methods=["GET"])
def health_check():
    return make_response("OK", 200)


@app.route("/api/v1/login", methods=["POST"])
def login():
    try:
        data = get_request_data(request, ["email", "password"])
    except (ValueError, TypeError) as e:
        return handle_error("Invalid parameters: %s" % str(e), 422)

    db = DatabaseService()
    userType = db.authenticate_user(
        email=data["email"], 
        password=data["password"],
    )
    if not userType:
        return make_response("Error: invalid credentials", 401)

    # add user data to encoded token
    tokenData = {
        "subject": data["email"],
        "userType": userType,
    }
    if userType == "student":
        tokenData["cohort"] = db.get_user(data["email"])["cohort"]

    token = jwt.encode(
        tokenData,
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    return jsonify({"token": token})


@app.route("/api/v1/reset-token/send", methods=["POST"])
def forgot_password():

    try:
        data = get_request_data(
            request,
            required_params=["email", "resetURL"],
        )
    except (ValueError, TypeError) as e:
        return handle_error("%s: %s" % (request.url, str(e)), 422)

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
    try:
        data = get_request_data(
            request,
            required_params=["token", "password", "passwordCheck"],
        )
    except (ValueError, TypeError) as e:
        return handle_error("%s: %s" % (request.url, str(e)), 422)

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


@app.route("/api/v1/user-exists", methods=["GET"])
def user_exists():
    try:
        data = get_request_data(
            request,
            required_params=["email"],
        )
    except(ValueError, TypeError) as e:
        return handle_error("%s: %s" % (request.url, str(e)), 422)

    db = DatabaseService()
    if db.get_user(data["email"]):
        return make_response("OK", 200)
    return make_response("Not found", 404)

