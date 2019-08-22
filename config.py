import os

DEBUG = False
SQLALCHEMY_DATABASE_URI = os.environ.get("DATA_BASE_URL", "sqlite:///data.db")
