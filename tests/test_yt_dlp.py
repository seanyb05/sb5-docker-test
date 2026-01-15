import requests

def push_url_to_db(target_url: str):
    # Use your NAS IP or 'localhost' if running on the same machine
    # Port 8000 matches your Portainer/Compose mapping
    api_endpoint = "http://localhost:8001/update-db"

    # This dictionary becomes the 'payload' in your FastAPI method
    payload = {
        "url": target_url,
        "description": "Video for yt-dlp",
        "priority": "high"
    }

    try:
        # 'json=' automatically handles header 'Content-Type: application/json'
        response = requests.post(api_endpoint, json=payload, timeout=10)

        # Check if the NAS returned a success (200) status
        response.raise_for_status()

        print(f"Server Response: {response.json()}")
        return response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Connection Error: {e}")
        return None


# Test the call
push_url_to_db("https://music.youtube.com/watch?v=0FD5BgW6q8Q&si=MFeEVQx2FOumBHfP")