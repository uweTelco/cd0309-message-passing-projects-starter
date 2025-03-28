import grpc
import person_pb2
import person_pb2_grpc
from app.udac_person.services import PersonService
import logging


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udac_person-gRPC")

class  PersonServiceServicer(person_pb2_grpc.PersonServiceServicer):
    def Get(self, request, context):
        # Retrieve all persons from the database using the service
        logger.info('Welcome to gRPC.')
        persons = PersonService.retrieve_all()
        logger.info('Persons from DB received.')
        # Create a PersonList message
        person_list = person_pb2.PersonList()
        
        # Translate each Person model instance into a gRPC Person message
        for person in persons:
            grpc_person = person_pb2.Person(
                id=str(person.id),
                first_name=person.first_name,
                last_name=person.last_name,
                company_name=person.company_name
            )
            # Add the gRPC Person message to the PersonList
            person_list.person.append(grpc_person)
        logger.info('Send result to receiver.')
        logger.info(person_list)
        return person_list