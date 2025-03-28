import os
import grpc
import person_pb2_grpc
from app.person_servicer import PersonServiceServicer
from concurrent import futures
from app import create_app
import logging
from logging import StreamHandler

# Unified logging setup before anything else
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root_logger.addHandler(handler)

# Explicit configuration for gRPC logger
grpc_logger = logging.getLogger('grpc')
grpc_logger.setLevel(logging.INFO)

logger = logging.getLogger('main')

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    person_pb2_grpc.add_PersonServiceServicer_to_server(PersonServiceServicer(), server)
    server.add_insecure_port('[::]:5001')
    server.start()
    logger.info('gRPC server initialized on port 5001')  # Changed log message
    return server

app = create_app(os.getenv("FLASK_ENV") or "test")

if __name__ == "__main__":
    grpc_server = serve_grpc()
    try:
        logger.info("Starting Flask server on port 5000")
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        pass
    finally:
        grpc_server.stop(0)
        logger.info("Graceful shutdown complete")
