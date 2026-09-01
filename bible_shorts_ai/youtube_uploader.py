import os
import json
from pathlib import Path
from typing import List
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config import YOUTUBE_CLIENT_SECRETS_FILE, YOUTUBE_TOKEN_FILE

# Scopes required to upload YouTube videos
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    """Authenticates using OAuth2 and returns a YouTube service resource."""
    creds = None
    if YOUTUBE_TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(YOUTUBE_TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not YOUTUBE_CLIENT_SECRETS_FILE.exists():
                raise FileNotFoundError(
                    f"YouTube client_secrets.json not found at {YOUTUBE_CLIENT_SECRETS_FILE}.\n"
                    "To enable auto-uploading to YouTube:\n"
                    "1. Go to https://console.cloud.google.com\n"
                    "2. Create a project and enable 'YouTube Data API v3'.\n"
                    "3. Create OAuth 2.0 Client ID credentials (Desktop app).\n"
                    f"4. Download and save the JSON file as: {YOUTUBE_CLIENT_SECRETS_FILE}"
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                str(YOUTUBE_CLIENT_SECRETS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(YOUTUBE_TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)

def upload_video_to_youtube(
    video_path: Path,
    title: str,
    description: str,
    tags: List[str],
    privacy_status: str = "public",
    publish_at: str = None
) -> str:
    """
    Uploads an MP4 video to YouTube with specified metadata.
    Supports scheduled publishing via publish_at (ISO 8601 UTC string).
    Returns the YouTube Video ID.
    """
    youtube = get_authenticated_service()

    status_dict = {
        "selfDeclaredMadeForKids": False
    }
    if publish_at:
        status_dict["privacyStatus"] = "private"
        status_dict["publishAt"] = publish_at
    else:
        status_dict["privacyStatus"] = privacy_status

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": tags,
            "categoryId": "27"  # Education
        },
        "status": status_dict
    }

    media = MediaFileUpload(
        str(video_path),
        chunksize=-1,
        resumable=True,
        mimetype="video/mp4"
    )

    print(f"[*] Uploading {video_path.name} to YouTube as '{title}' ({privacy_status})...")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  [+] Upload progress: {int(status.progress() * 100)}%")

    video_id = response.get("id")
    video_url = f"https://youtube.com/shorts/{video_id}"
    print(f"[✓] Video uploaded successfully! Link: {video_url}")
    return video_id
