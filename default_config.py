import os

#  Those names are defined by the libs. Flask or extensipns the app is using
DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
#  SQLALCHEMY_DATABASE_URI = "postgres://pqwmhdwe:4cL8XNslkokqShIPROySqi1w_D1ZFL_1@manny.db.elephantsql.com:5432/pqwmhdwe"
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
SECRET_KEY = os.environ.get("APP_SECRET_KEY")
UPLOADED_IMAGES_DEST= os.path.join("static", "images")
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = [
    "access",
    "refresh",
]  # allow blacklisting for access and refresh tokens
