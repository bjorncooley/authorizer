import requests

from flask import (
    Flask,
    jsonify, 
    make_response,
    request
)
from threading import Thread


class MockServer(Thread):
    def __init__(self, port=5000):
        super().__init__()
        self.port = port
        self.app = Flask(__name__)
        self.url = "http://localhost:%s" % self.port

        self.app.add_url_rule("/mailgun", view_func=self._return_ok, methods=["POST"])
        self.app.add_url_rule("/shutdown", view_func=self._shutdown_server)

    def _return_ok(self):
        return make_response("OK", 200)

    def _shutdown_server(self):
        if not 'werkzeug.server.shutdown' in request.environ:
            raise RuntimeError('Not running the development server')
        request.environ['werkzeug.server.shutdown']()
        return 'Server shutting down...'

    def shutdown_server(self):
        requests.get("http://localhost:%s/shutdown" % self.port)
        self.join()

    def run(self):
        self.app.run(port=self.port)
