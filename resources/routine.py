from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    jwt_required
)

from models.routine import RoutineModel
from schemas.routine import RoutineSchema
from libs.strings import gettext

routine_schema = RoutineSchema()
store_list_schema = RoutineSchema(many=True)


class Routine(Resource):
    @classmethod
    def get(cls, routine_id: int):
        routine = RoutineModel.find_by_id(routine_id)
        if routine:
            return routine_schema.dump(routine), 200

        return {"message": gettext("routine_not_found")}, 404

    @classmethod
    def post(cls, routine_id: int):

        routine_json = request.get_json()

        routine = routine_schema.load(routine_json, partial=(
            "date",
        ))


        try:
            routine.save_to_db()
        except:
            return {"message": gettext("routine_error_inserting")}, 500

        return routine_schema.dump(routine), 201

    @classmethod
    def delete(cls, routine_id: int):
        routine = RoutineModel.find_by_id(routine_id)
        if routine:
            routine.delete_from_db()
            return {"message": gettext("routine_deleted")}, 200

        return {"message": gettext("routine_not_found")}, 404

    @classmethod
    def put(cls, routine_id: int):
        routine_json = request.get_json()

        routine = RoutineModel.find_by_id(routine_id)

        if routine is None:
            routine = RoutineModel()

        routine.description = routine_json["description"]
        routine.class_given = routine_json["class_given"]

        if routine.id is not None:
            routine = routine_schema.load(routine_json)

        routine.save_to_db()

        return routine_schema.dump(routine), 200
