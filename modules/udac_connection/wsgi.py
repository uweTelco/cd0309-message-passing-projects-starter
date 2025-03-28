import os
import logging
from logging import StreamHandler
from app import create_app

# Set up logging to standard output
stream_handler = StreamHandler()
stream_handler.setLevel(logging.INFO)  # You can adjust the level to DEBUG, WARNING, etc.
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)

# Get the root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)  # Set the desired log level
root_logger.addHandler(stream_handler)

app = create_app(os.getenv("FLASK_ENV") or "test")
if __name__ == "__main__":
    app.run(debug=True)