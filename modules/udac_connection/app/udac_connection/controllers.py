from datetime import datetime

from app.udac_connection.models import Connection, Location, Person
from app.udac_connection.schemas import (
    ConnectionSchema
)
from app.udac_connection.services import ConnectionService,  PersonService
from flask import (
    request, 
    jsonify
)
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional
from werkzeug.exceptions import BadRequest

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("udac_connection", description="Connections via geolocation.")  # noqa

@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema(many=True))
    def get(self, person_id) -> ConnectionSchema:
        try:
            start_date_str = request.args.get("start_date")
            end_date_str = request.args.get("end_date")

            if not start_date_str or not end_date_str:
                raise BadRequest("start_date and end_date query parameters are required.")
            
            try:
                start_date: datetime = datetime.strptime(start_date_str, DATE_FORMAT)
                end_date: datetime = datetime.strptime(end_date_str, DATE_FORMAT)
            except ValueError as e:
                raise BadRequest(f"Invalid date format: {e}")
            
            distance: Optional[int] = request.args.get("distance", 5)
            try:
                distance = int(distance)
            except ValueError:
                raise BadRequest("Distance must be an integer.")

            results = ConnectionService.find_contacts(
                person_id=person_id,
                start_date=start_date,
                end_date=end_date,
                meters=distance,
            )
            return results
        
        except BadRequest as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500