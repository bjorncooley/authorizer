import os
SANDBOX_MAILGUN_KEY = "key-744ac88580d33c9c7a44e28956ff0182"
SANDBOX_MAILGUN_URL = "https://api.mailgun.net/v3/sandboxecc62105c1f5408c81be352704b30ae4.mailgun.org"

class APIConfig:
    MAILGUN_KEY = os.getenv("MAILGUN_KEY", SANDBOX_MAILGUN_KEY)
    MAILGUN_URL = os.getenv("MAILGUN_URL", SANDBOX_MAILGUN_URL)
    SECRET_KEY = os.getenv("SECRET_KEY", "notarealsecretkey")
