# app/person_servicer.py
import grpc
import person_pb2
import person_pb2_grpc
from flask import Flask
from app.udac_person.services import PersonService


class PersonServiceServicer(person_pb2_grpc.PersonServiceServicer):
    def __init__(self, flask_app: Flask):
        self.flask_app = flask_app  # Store the app reference
        self.logger = flask_app.logger.getChild("grpc")  # Use Flask's logger

    def Get(self, request, context):
        with self.flask_app.app_context():  # Use stored app's context
            try:
                self.logger.info('Starting gRPC Get handler')
                persons = PersonService.retrieve_all()
                
                person_list = person_pb2.PersonList()
                for person in persons:
                    person_list.person.append(
                        person_pb2.Person(
                            id=str(person.id),
                            first_name=person.first_name,
                            last_name=person.last_name,
                            company_name=person.company_name
                        )
                    )
                
                self.logger.info('Successfully processed %d persons', len(persons))
                return person_list
                
            except Exception as e:
                self.logger.error("gRPC Get failed: %s", str(e))
                context.abort(grpc.StatusCode.INTERNAL, f"Server error: {str(e)}")
