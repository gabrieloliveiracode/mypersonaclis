from ma import ma
from models.client import ClientModel
from models.routine import RoutineModel


class RoutineSchema(ma.ModelSchema):

    class Meta:
        model = RoutineModel
        load_only = ("client",)
        dump_only = ("id",)
        include_fk = True
