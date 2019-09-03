from flask_restful import Resource
from flask import request, g
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from flask_babel import gettext
import traceback
from sqlalchemy.exc import SQLAlchemyError
from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST
from libs.mailgun import MailGunException
from libs.exception import ApiError

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)

        if UserModel.find_by_username(user.username):
            raise ApiError(gettext(u"user_username_exists"), status_code=400)

        if UserModel.find_by_email(user.email):
            raise ApiError(gettext(u"user_email_exists"), status_code=400)

        try:
            user.save_to_db()
            return {"message": gettext("user_registered")}, 201
        except MailGunException as e:
            user.delete_from_db()  # rollback
            raise ApiError(str(e), status_code=500)
        except SQLAlchemyError as e:  # failed to save user to db
            error = str(e.__dict__['orig'])
            print(error)
            traceback.print_exc()
            user.delete_from_db()  # rollback
            raise ApiError(gettext(u"user_error_creating"), status_code=500)


class User(Resource):

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            raise ApiError(gettext(u"user_not_found"), status_code=404)

        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            raise ApiError(gettext(u"user_not_found"), status_code=404)

        user.delete_from_db()
        return {"message": gettext("user_deleted")}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=(
                                                    "email",
                                                    "name",
                                                    "surname",
                                                    "age",
                                                    "phone_number",
                                                    "cref",
        ))

        user = UserModel.find_by_username(user_data.username)

        if user and safe_str_cmp(user.password, user_data.password):
            access_token = create_access_token(user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return (
                {"access_token": access_token, "refresh_token": refresh_token, "locale": user.locale},
                200,
            )

        raise ApiError(gettext(u"user_invalid_credentials"), status_code=401)


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": gettext("user_logged_out").format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
