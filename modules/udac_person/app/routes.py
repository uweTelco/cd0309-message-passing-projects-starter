def register_routes(api, app, root="api"):
    from app.udac_person import register_routes as attach_udac_person

    # Add routes
    attach_udac_person(api, app)
