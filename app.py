from flask import Flask, jsonify, g
from flask_restful import Api, request
from flask_jwt_extended import JWTManager, get_jwt_identity
from flask_uploads import configure_uploads, patch_request_class
from marshmallow import ValidationError
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_babel import Babel, refresh

from db import db
from ma import ma
from blacklist import BLACKLIST
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from resources.client import Client, ClientList
from resources.routine import Routine

#  from resources.image import ImageUpload, Image, AvatarUpload, Avatar
from libs.image_helper import IMAGE_SET
from libs.exception import ApiError

app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
patch_request_class(app, 10 * 1024 * 1024)
configure_uploads(app, IMAGE_SET)
api = Api(app)
babel = Babel(app)

jwt = JWTManager(app)
migrate = Migrate(app, db)


@app.before_first_request
def create_tables():
    db.create_all()


@app.before_request
def set_locale():
    # define the user location
    user_locale = request.headers.get('Accept-Language')
    print(user_locale)
    # if there is no language set in the header
    if user_locale is None:
        g.user_locale = babel.default_locale
    else:
        g.user_locale = user_locale

    refresh()


@babel.localeselector
def get_locale():
    return g.user_locale


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


@app.errorhandler(ApiError)
def handle_api_error(error):
    return error.get_response()


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
#  api.add_resource(ImageUpload, "/upload/image")
#  api.add_resource(Image, "/image/<string:filename>")
#  api.add_resource(AvatarUpload, "/upload/avatar")
#  api.add_resource(Avatar, "/avatar/<int:user_id>")
api.add_resource(Client, "/v1/client/<int:client_id>", "/v1/client")
api.add_resource(ClientList, "/v1/clients")
api.add_resource(Routine, "/v1/routine/<int:routine_id>", "/v1/routine")


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(debug=True, port=5000)
