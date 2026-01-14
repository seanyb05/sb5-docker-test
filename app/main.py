import logging
import os
from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI()
now = datetime.now()

# Get the script's local directory
base_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(base_dir, f"{now}.log")

# Configure logger to write to the local file
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@app.post("/hello")
def index():
    return {"message": "Hello World"}

# @app.post("/log")
# async def log_post_message(request: Request):
#     # Receive the POST body
#     body = await request.json()
#
#     # Log the received message locally
#     logger.info(f"Received POST message: {body}")
#
#     return {"status": "Message logged locally", "data": body}
