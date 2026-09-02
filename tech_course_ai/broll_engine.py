import subprocess
import os
import requests
from pathlib import Path
from typing import Optional, List
from config import BROLL_DIR, TEMP_DIR, PEXELS_API_KEY, VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS

def search_and_download_pexels_video(query: str, target_path: Path) -> bool:
    """
    Searches Pexels for a real 1080p tech motion video clip and downloads the MP4.
    """
    if not PEXELS_API_KEY:
        return False
    
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={requests.utils.quote(query)}&per_page=5&orientation=landscape"
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            videos = r.json().get("videos", [])
            for v in videos:
                files = v.get("video_files", [])
                # Find 1080p HD file
                selected_link = None
                for f in files:
                    if f.get("width") == 1920 or f.get("quality") == "hd":
                        selected_link = f.get("link")
                        break
                if not selected_link and files:
                    selected_link = files[0].get("link")
                    
                if selected_link:
                    print(f"  [↓] Downloading real Pexels 1080p video for query '{query}'...")
                    resp = requests.get(selected_link, stream=True, timeout=45)
                    if resp.status_code == 200:
                        with open(target_path, "wb") as vid_file:
                            for chunk in resp.iter_content(chunk_size=65536):
                                vid_file.write(chunk)
                        print(f"  [✓] Downloaded real video: {target_path.name} ({target_path.stat().st_size // 1024} KB)")
                        return True
    except Exception as e:
        print(f"[!] Pexels video download error for '{query}': {e}")
    return False

def generate_procedural_cyber_video(duration: float, title_theme: str, output_path: Path):
    """
    Generates a dynamic 30fps moving Cyber-Grid / Tech matrix background video.
    """
    filter_complex = (
        f"color=c=0x090d14:s={VIDEO_WIDTH}x{VIDEO_HEIGHT}:d={duration+1}:r={VIDEO_FPS},"
        f"drawgrid=w=100:h=100:t=2:c=0x00e5ff@0.12,"
        f"drawgrid=w=500:h=500:t=3:c=0x00e5ff@0.25"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", filter_complex,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-t", f"{duration:.3f}",
        str(output_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path

def get_real_motion_broll_clip(
    query: str,
    duration: float,
    output_path: Path
) -> Path:
    """
    Returns a real 1080p motion video clip tailored for the section duration.
    """
    safe_name = "".join(c for c in query if c.isalnum() or c == "_")[:25]
    cached_broll = BROLL_DIR / f"pex_{safe_name}.mp4"
    
    if not (cached_broll.exists() and cached_broll.stat().st_size > 50000):
        search_and_download_pexels_video(query, cached_broll)

    # If downloaded successfully, scale and trim to duration
    if cached_broll.exists() and cached_broll.stat().st_size > 50000:
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1",
            "-i", str(cached_broll),
            "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,crop={VIDEO_WIDTH}:{VIDEO_HEIGHT}",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-t", f"{duration:.3f}",
            "-an",
            str(output_path)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path

    # Fallback to dynamic procedural tech background
    generate_procedural_cyber_video(duration, query, output_path)
    return output_path
