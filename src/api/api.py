from flask import (
    Flask,
    make_response,
)

app = Flask(__name__)

@app.route("/api/v1/health-check", methods=["GET"])
def health_check():
    return make_response("OK", 200)


@app.route("/api/v1/create-user", methods=["POST"])
def create_user():
    return make_response("OK", 200)