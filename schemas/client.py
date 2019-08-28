from ma import ma
from models.client import ClientModel
from models.routine import RoutineModel
from schemas.user import UserSchema


class ClientSchema(ma.ModelSchema):
    users = ma.Nested(UserSchema, many=True)

    class Meta:
        model = ClientModel
        load_only = ("user",)
        dump_only = ("id",)
        include_fk = True
