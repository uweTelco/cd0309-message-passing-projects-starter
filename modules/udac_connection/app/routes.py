def register_routes(api, app, root="api"):
    from app.udac_connection import register_routes as attach_udac_connection

    # Add routes
    attach_udac_connection(api, app)
