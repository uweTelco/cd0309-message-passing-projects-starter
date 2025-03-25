from app.udac_person.models import Person  # noqa
from app.udac_person.schemas import PersonSchema  # noqa


def register_routes(api, app, root="api"):
    from app.udac_person.controllers import api as udac_person_api

    api.add_namespace(udac_person_api, path=f"/{root}")
