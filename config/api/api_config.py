import os

class APIConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "notarealsecretkey")
