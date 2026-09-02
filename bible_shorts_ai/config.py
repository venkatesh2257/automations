import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
AUDIO_DIR = ASSETS_DIR / "audio"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"

for directory in [ASSETS_DIR, FONTS_DIR, AUDIO_DIR, OUTPUT_DIR, TEMP_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Video Settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 30
ZOOM_SPEED = 0.04  # Ken Burns effect speed

# Voice Settings (Microsoft Edge Neural Voices - Free)
# Top storyteller voices:
# - en-US-ChristopherNeural (Deep, dramatic, powerful)
# - en-US-GuyNeural (Narrator style)
# - en-US-AndrewNeural (Warm, clear)
# - en-GB-RyanNeural (British documentary style)
DEFAULT_VOICE = "en-US-ChristopherNeural"
VOICE_RATE = "-4%"   # Slightly slower for epic/dramatic delivery
VOICE_PITCH = "-2Hz" # Slightly deeper tone

# Subtitle Styling (TikTok / Shorts viral style)
FONT_NAME = "DejaVu Sans"  # Common Linux font, easily rendered
FONT_SIZE = 72
PRIMARY_COLOR = "&H00FFFFFF"   # White (ASS format: &HAABBGGRR)
HIGHLIGHT_COLOR = "&H0000FFFF" # Golden Yellow highlight
OUTLINE_COLOR = "&H00000000"   # Black border
OUTLINE_WIDTH = 5
SHADOW_DEPTH = 3

# Load .env if present
env_file = BASE_DIR / ".env"
if env_file.exists():
    with open(env_file, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

# AI & APIs
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
YOUTUBE_CLIENT_SECRETS_FILE = BASE_DIR / "client_secrets.json"
YOUTUBE_TOKEN_FILE = BASE_DIR / "token.json"

# Instagram Settings
INSTAGRAM_USERNAME = os.environ.get("INSTAGRAM_USERNAME", "")
INSTAGRAM_PASSWORD = os.environ.get("INSTAGRAM_PASSWORD", "")
INSTAGRAM_SESSION_FILE = BASE_DIR / "ig_session.json"

# Image Generation Defaults
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1920
IMAGE_MODEL = "flux"  # flux, turbo
CACHE_DIR = ASSETS_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
