from typing import List
from datetime import datetime
from db import db
from sqlalchemy.sql import func


class RoutineModel(db.Model):
    __tablename__ = "routines"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), nullable=False, unique=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, server_default=func.now())
    class_given = db.Column(db.Boolean, nullable=False)

    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    client = db.relationship("ClientModel")

    @classmethod
    def find_by_client(cls, client_id: int) -> List:
        return cls.query.filter_by(client_id=client_id).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "RoutineModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

