import logging
import os
from fastapi import FastAPI, Request, Response
from datetime import datetime

app = FastAPI()
now = datetime.now()

base_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(base_dir, f"{now}.log")

@app.post("/hello")
def index():
    return {"message": "Hello World"}

@app.post("/log")
async def log_post_message(request: Request):

    # Receive the POST body
    body = await request.json()

    return {"status": "Message logged locally", "data": body}

@app.get("/judgement")
async def get_judgement():
    return "you are bad"

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204) # 204 means "No Content"