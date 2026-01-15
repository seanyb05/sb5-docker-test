FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg
COPY . .
CMD uvicorn app.main:app --host 0.0.0.0 --reload --port 8001