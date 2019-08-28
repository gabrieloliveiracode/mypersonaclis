from ma import ma
from models.user import UserModel
from models.client import ClientModel


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
