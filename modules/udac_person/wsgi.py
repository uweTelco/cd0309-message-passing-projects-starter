import os
import grpc
import person_pb2_grpc
from app.person_servicer import PersonServiceServicer
from concurrent import futures
from app import create_app

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    person_pb2_grpc.add_PersonServiceServicer_to_server(PersonServiceServicer(), server)
    server.add_insecure_port('[::]:5001')
    server.start()
    return server

app = create_app(os.getenv("FLASK_ENV") or "test")

if __name__ == "__main__":
    grpc_server = serve_grpc()
    try:
        app.run(debug=True)  # Flask will run on the default port 5000
    finally:
        grpc_server.stop(0)  # Stop the gRPC server when the Flask app stops
