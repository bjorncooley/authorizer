from flask import (
    Flask,
    jsonify,
    make_response,
    request,
)
from flask_cors import CORS
import json
from jose import jwt
import logging
from pprint import pprint
import os
import random
import requests
import string
import sys

SRC_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(SRC_DIR)
sys.path.insert(0, SRC_DIR)
sys.path.insert(0, BASE_DIR)

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


def send_reset_link(email, token):

    mailgun_key = app.config["MAILGUN_KEY"]
    if not mailgun_key:
        logger.warning("No Mailgun Key in environment")
        return make_response("OK", 200)

    reset_link = "https://videos.missionu.com/reset-password/%s" % token
    mailgun_link = "https://api:%s@api.mailgun.net/v3/mg.missionu.com/messages" % mailgun_key
    data = {
        "from": "MissionU <mailgun@missionu.com>",
        "to": email,
        "subject": "Password reset link from MissionU",
        "text": "Please use this link to reset your password: %s" % reset_link,
    }
    return requests.post(mailgun_link, data=data)


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
    return jsonify(user)


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
    error = check_params(request, ["email"])
    if error:
        return error

    data = json.loads(request.data.decode('utf-8'))
    email = data["email"]
    token = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))

    mailgun_response = send_reset_link(email=email, token=token)
    if mailgun_response.status_code != 200:
        return make_response(
            '''There was an error sending your reset link,
            please email tech@missionu.com with this error: %s'''
            % mailgun_response.text)

    db = DatabaseService()
    db.save_token(email=email, token=token)
    return make_response("OK", 200)

