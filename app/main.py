import os
from fastapi import FastAPI, Request, Response, Body
from datetime import datetime
from pathlib import Path
import json
import subprocess

app = FastAPI()
now = datetime.now()

base_dir = Path(__file__).resolve().parent.parent
log_path = os.path.join(base_dir, f"{now}.log")
DB_FILE = Path(base_dir.joinpath("data").joinpath("db_url.txt"))

@app.post("/hello")
def index():
    return {"message": "Hello World"}

@app.post("/update-db")
async def add_to_top(payload: dict = Body(...)):
    # 1. Ensure directory exists
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)

    # 2. Convert JSON payload to a single string line
    new_entry = json.dumps(payload) + "\n"

    # 3. Read existing content
    existing_content = ""
    if DB_FILE.exists():
        existing_content = DB_FILE.read_text()

    # 4. Write new entry + old content (Prepend)
    DB_FILE.write_text(new_entry + existing_content)

    run_cmd()
    return {"message": "Data prepended successfully", "file": str(DB_FILE)}

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

def get_last_line(file_path="db_url.txt"):
    try:
        # 1. Read all lines
        with open(file_path, "r") as f:
            lines = f.readlines()

        if not lines:
            return None

        # 2. Extract the last line and keep the rest
        last_line = lines.pop().strip()

        return last_line
    except FileNotFoundError:
        return "File not found!"

def delete_last_line(file_path):
    try:
        # 1. Read all lines
        with open(file_path, "r") as f:
            lines = f.readlines()

        if not lines:
            return None

        # 2. Extract the last line and keep the rest
        lines.pop().strip()

        # 3. Overwrite file with remaining lines
        with open(file_path, "w") as f:
            f.writelines(lines)

        return 1
    except FileNotFoundError:
        return "File not found!"


def download_video(url: str,download_path):
    # 1. Define and create the folder if missing
    # 'parents=True' creates subfolders; 'exist_ok=True' ignores error if it exists

    # Construct the command as a list for security and reliability
    command = [
        "yt-dlp",
        "-P", download_path,
        url
    ]

    try:
        # Execute the command
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Download completed successfully!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")

def run_cmd():
    db_file_path = base_dir.joinpath("data").joinpath("db_url.txt")
    download_path = base_dir.joinpath("data").joinpath("downloads")
    download_path.mkdir(parents=True, exist_ok=True)

    last_json = get_last_line(db_file_path)
    data_dict = json.loads(last_json)
    last_url = data_dict["url"]
    download_video(last_url,download_path)
    delete_last_line(db_file_path)