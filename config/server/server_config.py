import os

class ServerConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "notarealsecretkey")
