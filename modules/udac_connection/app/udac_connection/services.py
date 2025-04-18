import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.udac_connection.models import Connection, Location, Person
from app.udac_connection.schemas import ConnectionSchema, LocationSchema, PersonSchema
from sqlalchemy.sql import text
import grpc
from person_pb2 import empty
from person_pb2_grpc import PersonServiceStub

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udac_connection-api")


class ConnectionService:
    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[Connection]:
        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """
        locations: List = db.session.query(Location).filter(
            Location.person_id == person_id
        ).filter(Location.creation_time < end_date).filter(
            Location.creation_time >= start_date
        ).all()
        logger.info('Received the locations')
        # Cache all users in memory for quick lookup
        person_map: Dict[str, Person] = {person.id: person for person in PersonService.retrieve_all()}
       
        # Prepare arguments for queries
        data = []
        for location in locations:
            data.append(
                {
                    "person_id": person_id,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                    "meters": meters,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
                }
            )

        query = text(
            """
        SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        AND     person_id != :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
        )
        result: List[Connection] = []
        with db.engine.connect() as connection:
            for line in data:
                result_set = connection.execute(query, {
                        'latitude': line['latitude'],
                        'longitude': line['longitude'],
                        'meters': line['meters'],
                        'person_id': line['person_id'],
                        'start_date': line['start_date'],
                        'end_date': line['end_date'],
                    })
                for exposed_person_id, location_id, exposed_lat, exposed_long, exposed_time in result_set:
                    location = Location(
                        id=location_id,
                        person_id=exposed_person_id,
                        creation_time=exposed_time,
                    )
                    location.set_wkt_with_coords(exposed_lat, exposed_long)

                    result.append(
                        Connection(
                            person=person_map[exposed_person_id], location=location,
                        )
                    )
        return result



class PersonService:


    @staticmethod
    def retrieve_all_old() -> List[Person]:
        return db.session.query(Person).all()
    @staticmethod
    def retrieve_all() -> List[Person]:
        """
        Retrives all persons from 
        """
        # Connect to the gRPC server
        logger.info('Starting gRPC')
        channel = grpc.insecure_channel('udac-person:5001')  # Ensure this matches your server address
        stub = PersonServiceStub(channel)
        logger.info('Stub received')
        # Prepare the empty request
        empty_request = empty()

        # Call the RPC
        #response = stub.Get(empty_request)
        try:
            response = stub.Get(empty_request)
        except grpc.RpcError as e:
            logger.info(f"gRPC call failed: {e}")
            return {"error": "Failed to fetch data"}, 500
        logger.info('Response received:')
        logger.info(response)
        # Map the response to your SQLAlchemy model and return list of Person objects
        persons = []
        for person in response.person:
            person_record = Person(
                id=int(person.id),
                first_name=person.first_name,
                last_name=person.last_name,
                company_name=person.company_name
            )
            persons.append(person_record)
        return persons
