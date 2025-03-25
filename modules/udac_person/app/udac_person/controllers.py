from datetime import datetime

from app.udac_person.models import Person
from app.udac_person.schemas import (
    PersonSchema
)
from app.udac_person.services import PersonService
from flask import request, jsonify
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect Person API", description="Connections via geolocation.")  # noqa


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        try:
            payload = request.get_json()
            new_person: Person = PersonService.create(payload)
            return new_person
        except BadRequest as e:
            return jsonify({"error": "Invalid data provided", "message": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred", "message": str(e)}), 500

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        try:
            persons: List[Person] = PersonService.retrieve_all()
            return persons
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred", "message": str(e)}), 500


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        try:
            person: Person = PersonService.retrieve(person_id)
            if not person:
                return jsonify({"error": "Person not found"}), 404
            return person
        except NotFound as e:
            return jsonify({"error": "Person not found", "message": str(e)}), 404
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred", "message": str(e)}), 500
