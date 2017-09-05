from flask import (
    Flask,
    make_response,
)

app = Flask(__name__)

@app.route("/health-check", methods=["GET"])
def health_check():
    return make_response("OK", 200)
