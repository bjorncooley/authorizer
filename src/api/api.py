from flask import (
    Flask,
    make_response,
    request,
)
import json

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

    return make_response("OK", 200)
