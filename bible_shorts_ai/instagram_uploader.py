import os
import sys
from pathlib import Path
from typing import Optional
from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, INSTAGRAM_SESSION_FILE

def get_instagram_client():
    """
    Initializes and logs in the Instagram client using instagrapi,
    reusing session settings if available to avoid repeated logins.
    """
    from instagrapi import Client
    
    cl = Client()
    # Emulate standard mobile device headers
    cl.set_user_agent("Instagram 300.0.0.29.110 Android (33/13; 420dpi; 1080x2400; Google/google; Pixel 7; cheetah; cheetah; en_US)")

    if INSTAGRAM_SESSION_FILE.exists():
        try:
            cl.load_settings(str(INSTAGRAM_SESSION_FILE))
            cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            return cl
        except Exception as e:
            print(f"[!] Saved Instagram session expired, re-logging in: {e}")

    if not INSTAGRAM_USERNAME or not INSTAGRAM_PASSWORD:
        raise ValueError(
            "Instagram credentials not found in .env.\n"
            "Please add:\n"
            "INSTAGRAM_USERNAME=your_instagram_handle\n"
            "INSTAGRAM_PASSWORD=your_instagram_password\n"
            "to /home/user/Desktop/automation/bible_shorts_ai/.env"
        )

    cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    try:
        cl.dump_settings(str(INSTAGRAM_SESSION_FILE))
    except Exception:
        pass
        
    return cl

def upload_reel_to_instagram(
    video_path: Path,
    caption: str,
    thumbnail_path: Optional[Path] = None
) -> Optional[str]:
    """
    Uploads a 1080x1920 MP4 video as an Instagram Reel.
    Returns the Reel URL or None if credentials are not configured.
    """
    if not INSTAGRAM_USERNAME and not INSTAGRAM_SESSION_FILE.exists():
        print("  [i] Instagram upload skipped (INSTAGRAM_USERNAME not set in .env).")
        return None

    try:
        print(f"[*] Connecting to Instagram (@{INSTAGRAM_USERNAME})...")
        cl = get_instagram_client()
        
        # Ensure a thumbnail JPG exists using FFmpeg
        thumb_file = thumbnail_path
        if not thumb_file or not thumb_file.exists():
            thumb_file = video_path.with_suffix(".jpg")
            import subprocess
            cmd = [
                "ffmpeg", "-y", "-ss", "00:00:02",
                "-i", str(video_path),
                "-vframes", "1",
                "-update", "1",
                str(thumb_file)
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f"[*] Uploading Reel '{video_path.name}' to Instagram...")
        media = cl.clip_upload(
            path=str(video_path.resolve()),
            caption=caption[:2200],
            thumbnail=str(thumb_file.resolve()) if thumb_file.exists() else None
        )
        
        reel_url = f"https://www.instagram.com/reel/{media.code}/"
        print(f"[✓] Instagram Reel uploaded successfully! Link: {reel_url}")
        return reel_url
    except Exception as e:
        print(f"[!] Instagram upload failed: {e}")
        return None
