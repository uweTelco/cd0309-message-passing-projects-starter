from app.udac_connection.models import Connection, Person  # noqa
from app.udac_connection.schemas import ConnectionSchema, LocationSchema, PersonSchema  # noqa


def register_routes(api, app, root="api"):
    from app.udac_connection.controllers import api as udac_connection_api

    api.add_namespace(udac_connection_api, path=f"/{root}")
