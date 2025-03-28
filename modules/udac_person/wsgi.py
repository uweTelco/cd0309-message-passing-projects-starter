from concurrent import futures
import grpc
from flask import Flask
from grpc_health.v1 import health_pb2_grpc
from app.person_servicer import PersonServiceServicer
from person_pb2_grpc import add_PersonServiceServicer_to_server
from app import create_app
from health import HealthService

def serve_grpc(flask_app):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    
    # Pass flask_app to the servicer
    add_PersonServiceServicer_to_server(
        PersonServiceServicer(flask_app), 
        server
    )
    
    health_pb2_grpc.add_HealthServicer_to_server(
        HealthService(),
        server
    )
    
    server.add_insecure_port('[::]:5001')
    return server

# Create Flask app FIRST
app = create_app()

# Initialize gRPC server WITH app reference
grpc_server = serve_grpc(app)

if __name__ == '__main__':
    grpc_server.start()
    
    # Push app context for Flask initialization
    with app.app_context():
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
