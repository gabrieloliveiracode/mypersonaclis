from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    jwt_required
)

from models.client import ClientModel
from schemas.client import ClientSchema
from libs.strings import gettext

client_schema = ClientSchema()
client_list_schema = ClientSchema(many=True)


class Client(Resource):
    @classmethod
    def get(cls, client_id: int):
        client = ClientModel.find_by_id(client_id)
        if client:
            return client_schema.dump(client), 200

        return {"message": gettext("client_not_found")}, 404

    @classmethod
    def post(cls):

        client_json = request.get_json()
        client = ClientModel.find_by_email(client_json["email"])

        if client:
            return {"message": gettext("client_name_exists").format(client.name)}, 400

        client = client_schema.load(client_json)

        try:
            client.save_to_db()
        except:
            return {"message": gettext("client_error_inserting")}, 500

        return client_schema.dump(client), 201

    @classmethod
    def delete(cls, client_id: int):
        client = ClientModel.find_by_id(client_id)
        if client:
            client.delete_from_db()
            return {"message": gettext("client_deleted")}, 200

        return {"message": gettext("client_not_found")}, 404

    @classmethod
    def put(cls, client_id: int):
        client_json = request.get_json()
        client = ClientModel.find_by_id(client_id)

        if client is None:
            client = ClientModel()

        client.name = client_json["name"]
        client.email = client_json["email"]
        client.age = client_json["age"]
        client.phone_number = client_json["phone_number"]
        client.user_id = client_json["user_id"]

        client.save_to_db()

        return client_schema.dump(client), 200


class ClientList(Resource):
    @classmethod
    def get(cls):
        return {"clients": client_list_schema.dump(ClientModel.find_all())}, 200
